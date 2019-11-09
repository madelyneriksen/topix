Topix - Functional Microframework for Redis Streams
=======

Topix is a functional microframework to work on Redis streams as infinite iterators.

## Get Started 🚀

Install Topix with the following commands:

```bash
virtualenv .env
source .env/bin/activate # Linux/OSX
.env\scripts\activate # Windows
pip install -r requirements.txt
python setup.py install

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
