SHELL=/bin/bash
VERSION=$(shell cat VERSION)

.PHONY: build test format clean
build: test dist/topix-${VERSION}.tar.gz

dist/topix-${VERSION}.tar.gz: .env/bin/activate
	python setup.py sdist bdist_wheel

test:
	pytest
	mypy --strict topix
	black --check topix

format:
	black topix

clean:
	rm -rf *.egg-info .eggs build dist
	rm -rf .coverage .pytest_cache __pycache__ .mypy_cache
