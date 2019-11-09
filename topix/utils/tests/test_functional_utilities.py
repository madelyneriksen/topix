"""Tests for functional utilities."""


from unittest import mock

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
