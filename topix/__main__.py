"""Command line script."""


import typing as t

import argparse
import logging
import json
import sys

from importlib import import_module


from topix.emitter import emit, CastType
from topix.stream import stream_into


# I am not even going to pretend this is typesafe...
def import_from(path: str) -> t.Any:
    """Import something from a python path."""
    module, item = path.split(":")
    return getattr(import_module(module), item)


def emitter(stream: str, mapping: t.Dict[CastType, CastType], **_: t.Any) -> None:
    """Emit a mapping to a stream from the command line."""
    emit(stream, mapping)


def consumer(
    stream: str,
    group: str,
    function: str,
    consumer: t.Optional[str] = None,
    concurrency: t.Optional[int] = None,
    **_: t.Any,
) -> None:
    """Consume events from the stream with a function."""
    fn = import_from(function)
    stream_into(fn, stream, group, consumer=consumer)


def _create_parsers() -> argparse.ArgumentParser:
    """Create a parser for the program."""
    parser = argparse.ArgumentParser(description=main.__doc__, prog="topix")

    # Global pieces, like logging configuration.
    parser.add_argument(
        "--log-format", default="%(levelname)s | %(name)s | %(asctime)s | %(message)s"
    )
    parser.add_argument("--log-level", default="INFO")

    subparsers = parser.add_subparsers()

    emit_parser = subparsers.add_parser("emitter", help=emitter.__doc__)
    emit_parser.add_argument("stream", type=str, help="Name of the stream to emit to.")
    emit_parser.add_argument(
        "mapping", type=json.loads, help="JSON-compatible string to emit."
    )
    emit_parser.set_defaults(func=emitter)

    consume_parser = subparsers.add_parser("consumer", help=consumer.__doc__)
    consume_parser.add_argument(
        "stream", type=str, help="Name of the stream to consume events from"
    )
    consume_parser.add_argument(
        "group", help="Name of the Redis consumer group to participate in"
    )
    consume_parser.add_argument(
        "function", type=str, help="Import path to the function (ex. 'app.myfunction')",
    )
    consume_parser.add_argument(
        "--consumer", type=str, help="Unique identifier for this consumer."
    )
    consume_parser.add_argument(
        "--concurrency", type=int, help="Number of threads to run the function with."
    )
    consume_parser.set_defaults(func=consumer)

    return parser


def main(raw_arguments: t.List[str]) -> None:
    """Topix CLI - Control Topix processes and streams.
    
    The command line allows the starting of "worker" processes,
    along with other miscellaneous tasks.
    """
    parser = _create_parsers()
    args = parser.parse_args(raw_arguments)
    logging.basicConfig(format=args.log_format, level=args.log_level)
    args.func(**vars(args))


if __name__ == "__main__":
    main(sys.argv[1:])
