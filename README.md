Topix
=======

A functional microframework to use Redis streams as infinite generators in Python.

## Quickstart 🚀

Install Topix:

```bash
pip install topix
```

Write a consumer function:

```python
# app.py

def consumer(data):
    print(data)
```

With Redis running on `localhost:6379`, listen for new items in a stream:

```bash
python -m topix consumer demo_stream printer_group app:consumer
```

Then, send items to the stream using the command `topix emitter`:

```bash
python -m topix emitter demo_stream '{"hello": "world"}'
```

...or using Python code:

```python
from topix import emit

emit("demo_stream", {"hello": "world"})
```

That's it. That's the API.

## Why Topix? 

I created Topix with a few primary goals and concepts:

* Topix has a dead-simple API- the "for humans" approach.
* Small abstraction over the fantastic Redis Streams.
* Implementation of Topix should favor simple code over new features.

## Usage

Topix centers around two concepts: _consumers_, implemented as functions, and _emitters_, that call `topix.emit` or `redis.xadd`.

### Writing a Consumer Function

With Topix, creating a consumer for a stream is as easy as creating a function. For example, this is a valid consumer function:

```python
def print_item(item):
    print(item)
```

Specifically, your function needs to be of the following _type_, otherwise you'll get an error:

```python
Callable[[Dict[bytes, bytes]], None]
```

Like Redis, Topix works with bytes, so if you want strings (or any other type) you need to bring your own converter.

### Using Your Consumer Function

Back to our `print_item` function, we can use this function in a consumer process using the Topix command line. Assuming we saved `print_item` in `app.py`, we can run Topix like this:

```bash
python -m topix consumer stream_name group_name app:print_item
```

Where `stream_name` is the name of the Redis stream, `group_name` is the name of the consumer group, and `app:print_item` is the Python path to our function (think `gunicorn`-style imports). By default, Topix will attempt to connect to the Redis url defined in the environment variable `TOPIX_REDIS_URL`, falling back to `redis://localhost:6379/0`.

At runtime, Topix will import your function, and map it over the stream you give it. Topix automatically handles acknowledging successful commands, the creation of consumer groups, removing the consumer when it exits, and parallel execution of your function using threads.

### Sending to Streams

Topix defines an `emit` function that sends a Redis-compatible dictionary to the stream you give it, by name:

```python
from topix import emit

emit("stream_name", {b"hello": b"world"})

# Strings are valid as keys too- they just
# become bytes "on the other side"
emit("stream_name", {"hello": "world"})
```

Topix's `emit` is a _thin_ wrapper around Redis' `XADD` command, and maps the values given to `XADD` to your consumer function. This means you can emit messages from _anywhere_, even from code in another language or not using Topix, and use your same consumer.

Typically, you'll want to emit events to your code using `emit` (or `xadd`) programmatically, but for demos (or `bash` scripts), Topix includes a subcommand to send messages to a stream:

```bash
python -m topix emit stream_name '{"hello": "world"}'
```

### Additional Configuration

By default, Topix uses a number of threads equivalent to the number of CPUs available. You can change the amount of concurrency (using threads) that Topix uses by providing the `--concurrency` option to `topix consumer`:

```bash
python -m topix consumer stream_name group_name app:print_item --concurrency 2
```

In addition, Topix supports a few additional options, including configurable logging. For a full list of options, try:

```bash
python -m topix --help
```

## Development

To get started hacking on Topix, be sure to install it in development mode.

```bash
virtualenv .env
source .env/bin/activate # Linux/OSX
.env\scripts\activate # Windows
pip install -r requirements.dev.txt
python setup.py develop
```

Tests are provided by Pytest. Plugins for `pylint` and `coverage` are directly integrated:

```bash
pytest # or python setup.py test
# Pytest Output

Coverage Report:

...

====== X Passed, X Skipped in .38 seconds =====
```

Topix checks types with MyPy. Type check your code like this:

```bash
mypy topix
```

## License

Copyright 2019 by Madelyn Eriksen under the terms of the MIT License. See [license](/LICENSE) for full terms.
