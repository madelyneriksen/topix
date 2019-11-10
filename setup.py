"""Setup file for topix"""


import setuptools


with open("README.md", "r") as fh:
    DESC = fh.read()

with open("VERSION", "r") as ver:
    VERSION = ver.read()


setuptools.setup(
    name="topix",
    version=VERSION,
    author="Madelyn Eriksen",
    author_email="opensource@madelyneriksen.com",
    description="Topix is a functional microframework for working with Redis streams.",
    long_description=DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/madelyneriksen/topix",
    packages=setuptools.find_packages(),
    setup_requires=[
        'pytest-runner>=2.0',
    ],
    install_requires=[
        'redis>=3.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
