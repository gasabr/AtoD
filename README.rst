====
AtoD
====
DotA2 data for ML.

What and why
============
DotA2 API gives you a lot of information about matches, leagues, players, 
but there's no way to get the data about game itself: heroes, their abilities etc.
This library helps with this task. And there is short summary of features:

- tools to extract data from in-game files (heroes attributes, abilities specs)
- classes Hero, Ability... to represent the data
- some examples of usage

Examples
========
Create a hero from name and get some basic info.

    >>> from atod import Hero
    >>> am = Hero.from_name('Anti-Mage') # produces the same result as above
    >>> am.str
    22
    >>> print(am.abilities)
    <Abilities [<Ability name=mana_break>, <Ability name=blink>, <Ability name=spell_shield>, <Ability name=mana_void>, ]>
    >>> am.lvl = 15 
    >>> am.str
    38


The code above creates Anti-Mage, which has some basic attributes: strength,
agility, armor all of them are counted at the run-time, so if you will change the
level of hero, attributes will change too.
Other examples of usage the Hero class can be found at examples/hero_data.ipynb.
Also you can use ``dir(Hero)`` to get all available properties of the Hero class.
