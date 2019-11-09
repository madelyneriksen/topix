"""Test the streaming API."""


from unittest import mock

import redis

from topix.stream import (
    lifecycle,
    stream_into,
)


@mock.patch("topix.stream.connection")
def test_stream_lifecycle(conn_mock):
    """teardown() ensures there's no extra consumers on Redis."""
    stream = "logs"
    group = "logger"
    consumer = "my_logger"

    with lifecycle(stream, group, consumer):
        pass
    conn_mock().xgroup_delconsumer.assert_called_once_with(stream, group, consumer)
    conn_mock().xgroup_create.assert_called_once_with(stream, group, mkstream=True)


@mock.patch("topix.stream.connection")
def test_stream_lifecycle_when_setup(conn_mock):
    """When a group and stream is already created, an error is raised and ignored."""
    stream = "logs"
    group = "logger"
    consumer = "my_logger"

    conn_mock().xgroup_create.side_effect = redis.exceptions.ResponseError
    with lifecycle(stream, group, consumer):
        pass


@mock.patch("topix.stream.connection")
def test_stream_into(conn_mock):
    """Test streaming into a function."""
    stream = "logs"
    group = "logger"
    fn = mock.MagicMock()

    conn_mock().xreadgroup.return_value = [
        [b"logs", [(b"ruid_stub", {b"msg": b"hello world"})]]
    ]

    with mock.patch("topix.stream.concurrently") as executor:
        stream_into(fn, stream, group)

        # Call the executor once to assert data unpacking works as
        # expected.
        next(executor.call_args[0][0])

    fn.assert_called_once_with({b"msg": b"hello world"})
    conn_mock().xack.assert_called_once_with(stream, group, b"ruid_stub")
    conn_mock().xreadgroup.assert_called_once()
