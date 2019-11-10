"""Streams module - functions that interact with Redis streams."""


import logging

import typing as t
import multiprocessing as mp

from functools import partial as p
from contextlib import contextmanager

import redis

from topix.utils import (
    concurrently,
    lazy_unpack,
    split_into,
    consume,
    generator,
    connection,
    guid,
)


T = t.TypeVar("T")


# Mapping stored in Redis streams.
StreamData = t.Dict[bytes, bytes]
StreamEntry = t.Tuple[bytes, StreamData]


log = logging.getLogger(__name__)


def _trim(x: t.List[t.Tuple[t.Any, T]]) -> T:
    """Removes extranneous data from Redis xreadgroup."""
    return x[0][1]


def _setup(stream: str, group: str) -> None:
    """Setup a stream with a consumer group on Redis."""
    try:
        connection().xgroup_create(stream, group, mkstream=True)  # type: ignore
        log.info("Created group=%s in stream=%s", group, stream)
    except redis.exceptions.ResponseError:
        log.info("Already created group=%s in stream=%s", group, stream)


def _teardown(stream: str, group: str, consumer: str) -> None:
    """Teardown a consumer in the group and stream."""
    log.warning(
        "Removing consumer=%s from group=%s on stream=%s", consumer, group, stream
    )
    connection().xgroup_delconsumer(stream, group, consumer)  # type: ignore


@contextmanager
def lifecycle(stream: str, group: str, consumer: str) -> t.Iterator[None]:
    """Redis stream lifecycle."""
    _setup(stream, group)
    try:
        yield
    finally:
        _teardown(stream, group, consumer)


def stream_into(
    fn: t.Callable[[StreamData], None],
    stream: str,
    group: str,
    consumer: t.Optional[str] = None,
    concurrency: int = mp.cpu_count(),
) -> None:
    """Feed entries from a Redis stream into a callable fn()

    Imagining a Redis stream as an infinite iterator, stream_into() applies
    the function fn to each element of the stream.

    Under the hood, stream_into() makes use of Python's concurrency primitives
    to allow for better performance of IO-heavy tasks on a consumer.

    Arguments:
        fn: Callable to map over elements of the stream.
        stream: Name of the redis stream.
        group: Name of the consumer group.
    Keyword Arguments:
        consumer: ID of the consumer to use. By default, a random UUIDv4
        concurrency: Number of threads to use. By default, the number of CPUs.
    Returns:
        None
    """
    consumer = consumer or guid()
    client = connection()

    # Functions to interact with Redis
    read = p(client.xreadgroup, group, consumer, {stream: ">"}, block=0)
    xack = p(client.xack, stream, group)

    # Transform nested redis-py xreadgroup response into an infinite lazy generator.
    source: t.Iterator[StreamEntry] = lazy_unpack(map(_trim, generator(read)))
    mapped = map(split_into(xack, fn), source)

    with lifecycle(stream, group, consumer):
        concurrently(mapped, threads=concurrency)
