import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "AtoD",
    version = "0.0.1",
    author = "Abroskin Gleb",
    author_email = "abroskingleb@gmail.com",
    description = ("Easy access to DotA2 internal data."),
    license = "MIT",
    keywords = "games data DotA2 ml",
    url = "https://github.com/gasabr/AtoD",
    packages=['atod', 'atod.utils', 'atod.tests', 'atod.db_models',
              'atod.models', 'atod.db'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5"
    ],
    install_requires=[
        "dota2api",
        "pandas",
        "sklearn",
        "SQLAlchemy",
        "yamjam",
        "scipy",
    ],
    include_package_data=True,
)
