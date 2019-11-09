"""Tests for dynamic importing."""


from topix.__main__ import import_from


def test_importing_from_dotpath():
    """Try to import some stuff from topix."""

    guid = import_from("topix.utils.guid")
    assert isinstance(guid(), str)
