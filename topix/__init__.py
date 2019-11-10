"""Topix - Functional Microframework for Redis Streams

Topix is a microframework to create event streams in Redis, using
a functional programming style in Python.
"""


import logging

from .emitter import emit
from .stream import stream_into

logging.getLogger(__name__).addHandler(logging.NullHandler())
