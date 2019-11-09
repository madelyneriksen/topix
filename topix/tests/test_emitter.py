"""Test the event emitter."""


from unittest import mock

from topix.emitter import emit


@mock.patch("topix.emitter.connection")
def test_stream_emitter(conn_mock):
    """Test the emitter works as expected."""
    emit("logs", {"msg": "A new user signed up."})
    conn_mock().xadd.assert_called_once_with("logs", {"msg": "A new user signed up."})

    conn_mock().xadd.reset_mock()

    emit("logs", {"msg": "Another new user signed up."})
    conn_mock().xadd.assert_called_once_with(
        "logs", {"msg": "Another new user signed up."}
    )


@mock.patch("topix.emitter.connection")
def test_stream_emitter_with_limits(conn_mock):
    """Test the stream emitter allows limiting stream history."""
    emit("logs", {"msg": "A new user signed up."}, limit=100_000)
    conn_mock().xadd.assert_called_once_with(
        "logs", {"msg": "A new user signed up."}, maxlen=100_000, approximate=True
    )
