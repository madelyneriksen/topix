"""Tests for functional utilities."""


from unittest import mock

import pytest

from topix.utils import (
    concurrently,
    split_into,
    consume,
    generator,
    connection,
)


def test_split_into():

    x = mock.MagicMock()
    y = mock.MagicMock()

    val = ("Hello", "World!")

    z = split_into(x, y)
    result = z(val)

    x.assert_called_once_with("Hello")
    y.assert_called_once_with("World!")

    assert result == x("Hello")


def test_consume():
    """Test consume function exausts iterator."""
    iterator = iter([1, 2, 3, 4])
    consume(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


@mock.patch("topix.utils.redis")
def test_connection_creator_is_singleton(redis_mock):
    """Test the connection creator doesn't create duplicate clients."""
    one = connection()
    two = connection()

    assert one is two
    redis_mock.Redis.from_url.assert_called_once_with("redis://localhost:6379/0")
