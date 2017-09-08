''' This is the library for getting DotA2 insight information. 

Problem:
    there was no way to get dota internal data about heroes, their abilities...
    in suitable for further work form.

Solution:
    this library allows you to get access to all the data in the in-game files.
    But information about single hero does not have much use, so there is a
    way to get stats of selected heroes or get information about certain
    match.

'''

from atod.meta import meta_info
from atod.models.interfaces import Member, Group
from atod.models.ability import Ability
from atod.models.abilities import Abilities
from atod.models.hero import Hero
from atod.models.heroes import Heroes
from atod.models.match import Match
from atod.utils.pick import get_recommendations
#  from atod.utils import dota_api
