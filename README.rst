====
AtoD
====
DotA2 data for ML.


Installation
============
Package can be installed with pip:

.. code-block:: bash

    $ pip install atod

To use Match class you should get your own DotA2 API key here_ and add it to
YamJam_ config file which can be found at `~/.yamjam/config.yaml`. If you don't have one
just create it with

.. code-block:: bash

    touch ~/.yamjam/config.yaml

.. _here http://steamcommunity.com/dev/apikey
.. _YamJam http://yamjam.readthedocs.io/en/latest/

After that add the following text to your config file:

.. code-block:: yaml

   AtoD:
     DOTA2_API_KEY: <your API key>

example:

.. code-block:: yaml

   AtoD:
     DOTA2_API_KEY: 65DCCD4C2595F8E7055797033214EE6F


Examples
========
Please, take a look at jupyter notebooks in `examples/` folder to see how the lib can be used.
Create a hero from name and get some basic info.

.. code-block:: python

    >>> from atod import Hero
    >>> am = Hero.from_name('Anti-Mage')
    >>> am.str
    22
    >>> print(am.abilities)
    <Abilities [<Ability name=mana_break>, <Ability name=blink>, <Ability name=spell_shield>, <Ability name=mana_void>, ]>
    >>> am.lvl = 15
    >>> am.str
    43


The code above creates Anti-Mage, which has some basic attributes: strength (str),
agility, armor all of them are counted at the run-time, so if you will change the
level of hero, attributes will change too.

Other examples of usage of the Hero class can be found at `examples/hero_data.ipynb.`


Documentation
=============
Auto generated docs can be found at ``docs/_build/html/index.html``.
I have tried to write reasonable documentation following Google style guide to
every module, file, function and unclear line. So, your editor will be able to 
load at least type annotations to all the functions (if you have one for sure).

Try the following code to display docs about Heroes class:

.. code-block:: python

    >>> from atod import Heroes
    >>> help(Heroes)
    ...


Issues
======
If you have any issues, please, write me an email: *contact@gasabr.me*
