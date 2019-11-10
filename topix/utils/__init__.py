"""Utilities used for Topix."""


import os

import typing as t
import multiprocessing.dummy as mp

from functools import lru_cache
from uuid import uuid4

from collections import deque
from uuid import uuid4

import redis


# There's a few higher order functions in here- we need some
# type variables.
T = t.TypeVar("T")
A = t.TypeVar("A")
B = t.TypeVar("B")


@lru_cache(maxsize=1)
def connection() -> redis.Redis:
    """Creates a singleton Redis client."""
    # Allow configuration of what env var to use.
    url = os.getenv("TOPIX_REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(url)


def generator(fn: t.Callable[[], T]) -> t.Iterator[T]:
    """Turn a callable function into an infinite generator."""
    while True:
        yield fn()


def consume(iterable: t.Iterator[T]) -> None:
    """Completely consume an iterable. Usually used with map()"""
    deque(iterable, maxlen=0)


def lazy_unpack(iterable: t.Iterator[t.Iterator[T]]) -> t.Iterator[T]:
    """Convert an iterator of iterators into an iterator of items.

    iter([[x, y, z], [a, b, c]]) -> iter([x, y z, a, b, c])
    """
    for member in iterable:
        yield from member


def concurrently(iterable: t.Iterator[T], threads: int = 4) -> None:
    """Concurrently iterate through an iterable.

    Arguments:
        iterable: Iterator to move through.
    Keyword Arguments:
        threads: Number of threads to use.
    Returns:
        None
    """
    with mp.Pool(threads) as p:
        p.map(consume, iterable)


def split_into(
    x: t.Callable[[A], T], y: t.Callable[[B], None]
) -> t.Callable[[t.Tuple[A, B]], T]:
    """Create a function to unpack a tuple and use one as a side effect."""

    def z(val: t.Tuple[A, B]) -> T:
        """Send val[0] to x, val[0] to y, and return x(val[0])."""
        a, b = val
        result = x(a)
        y(b)
        return result

    return z


def guid() -> str:
    """Create a random UUID4 string."""
    return str(uuid4())
