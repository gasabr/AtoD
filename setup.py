import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "atod",
    version = "0.1.0",
    author = "Abroskin Gleb",
    author_email = "abroskingleb@gmail.com",
    description = ("An interactive Dota2 wiki."),
    license = "MIT",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/atod",
    packages=['atod', 'atod.tools', 'atod.tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
    ],
)
