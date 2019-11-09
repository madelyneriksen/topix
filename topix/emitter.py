"""Emit messages to the stream."""


import typing as t

from topix.utils import connection


CastType = t.Union[str, int, bytes]


def emit(
    stream: str, data: t.Dict[CastType, CastType], limit: t.Optional[int] = None
) -> None:
    """Emit messages to the Redis stream.

    While `emit` accepts messages with values that are strings, integers,
    or bytes, the types are automatically cast to `bytes` before submission
    to the stream, and are similarly `bytes` when being read.

    To send more complex objects over Redis, consider using a serialization
    format like Pickle or JSON, and storing the bytes that way.

    Arguments:
        stream: Name of the stream to emit to.
        data: Data to send to the stream.
    Returns:
        None
    """
    client = connection()
    if limit is not None:
        client.xadd(stream, data, maxlen=limit, approximate=True)  # type: ignore
    else:
        client.xadd(stream, data)  # type: ignore
