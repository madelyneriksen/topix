"""Extremely simple demo functions."""


import typing as t
import logging


log = logging.getLogger(__name__)


def process(data: t.Dict[bytes, bytes]) -> None:
    """Prints the incoming data to stdout."""
    log.info("GOT DATA: %s", data)
