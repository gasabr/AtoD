====
AtoD
====
An Interactive DotA2 wiki.

This is a library which provides interface for DotA2 data in the suitable for
Machine Learning tasks form.

.. highlight:: python

::
    from atod import Hero

    am = Hero(1) # 1 is Anti-Mage's id
    am = Hero.from_name('Anti-Mage') # produces the same result as above

The code above creates Anti-Mage, which has some basic attributes: strength,
agility, armor all of them are counted on the fly, so if you will change the
level of hero, attributes will change too.

Use ``dir(Hero)`` to get all available properties of the Hero class.

::
    am_abilities = am.abilities.get_list()

Every hero has abilities, they are represented by special class -- Abilities.
Abilities contain some members -- list of Ability objects. Ability contain 4
main components:

- texts: description, lore, notes (all this is shown on ability card in the
game)
- specs: a lot of variables with string and numeric values. The database
contains "cleaned" version of abilities. What "cleaned" means will be
described later
- labels: abstract variables (~35) which should replace long specifications