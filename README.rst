====
AtoD
====
DotA2 data for ML.

Goals
=====
- create an API to get any DotA related data as easy as possible and ready for ML experiments
- create hero recommendation engine
- create web interface with interactive representation of the info

What and why
============
First of all it's educational project which is created to learn some staff, hope someone will find it useful.

DotA2 API gives you a lot of information about matches, leagues, players,
but there's no way to get the data about game itself: heroes, their abilities etc.
This library helps with this task. And there is short summary of features:

- tools to extract data from in-game files (heroes attributes, abilities specs)
- classes Hero, Ability... to represent the data
- some examples of usage

Examples
========
Please, take a look at jupyter notebooks in `examples/` folder to see how the lib can be used.
Create a hero from name and get some basic info.

    >>> from atod import Hero
    >>> am = Hero.from_name('Anti-Mage') # produces the same result as above
    >>> am.str
    22
    >>> print(am.abilities)
    <Abilities [<Ability name=mana_break>, <Ability name=blink>, <Ability name=spell_shield>, <Ability name=mana_void>, ]>
    >>> am.lvl = 15
    >>> am.str
    43


The code above creates Anti-Mage, which has some basic attributes: strength,
agility, armor all of them are counted at the run-time, so if you will change the
level of hero, attributes will change too.

Other examples of usage of the Hero class can be found at `examples/hero_data.ipynb.`
Auto generated docs can be found at ``docs/doxygen/html/index.html``.
