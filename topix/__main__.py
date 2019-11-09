"""Command line script."""


import typing as t
import json
import sys

import argparse


def emitter(stream: str, mapping: t.Dict[bytes, bytes]) -> None:
    """Emit a mapping to a stream from the command line."""


def consumer(
    stream: str, group: str, import_path: str, consumer_id: t.Optional[str] = None
) -> None:
    """Consume events from the stream with a function."""


def _create_parsers() -> argparse.ArgumentParser:
    """Create a parser for the program."""
    parser = argparse.ArgumentParser(description=main.__doc__, prog="topix")

    subparsers = parser.add_subparsers()

    emit_parser = subparsers.add_parser("emit", help=emitter.__doc__)
    emit_parser.add_argument("stream", type=str, help="Name of the stream to emit to.")
    emit_parser.add_argument(
        "mapping", type=json.loads, help="JSON-compatible string to emit."
    )

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
        "--consumer-id", type=str, help="Unique identifier for this consumer."
    )

    return parser


def main(raw_arguments: t.List[str]) -> None:
    """Topix CLI - Control Topix processes and streams.
    
    The command line allows the starting of "worker" processes,
    along with other miscellaneous tasks.
    """
    parser = _create_parsers()
    parser.parse_args(raw_arguments)


if __name__ == "__main__":
    main(sys.argv[1:])
