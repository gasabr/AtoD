#!/usr/bin/env python3
import os
import json
import requests
from bs4 import BeautifulSoup

from HeroModel import HeroModel
import config

features_list = ['primary_attr', 'str', 'str_gain', 'agi', 'agi_gain',
                 'int', 'int_gain', 'total', 'total_gain', 'total_lvl25',
                 'mov_speed', 'armor_base', 'dmg_base_min', 'dmg_base_max',
                 'range', 'basic_attack_time','attack_point', 'attack_base_time',
                 'vision_day', 'vision_night', 'turn_rate', 'collision',
                 'hp_regen_base', 'legs']


def create_heroes_summary():
    ''' Creates dict where key is hero name value - summary.

        Summary will contain id and information
        about hero role from the game client (6.87).
        In DATA_FOLDER folder there is dict id -> summary this function
        reverse it.
    '''

    id_to_sum = {}
    filename = os.path.join(config.DATA_FOLDER, 'heroes-features.json')
    with open(filename, 'r') as fp:
        id_to_sum = json.load(fp)

    heroes_summary = {}
    for hero_id, summary in id_to_sum.items():
        hero_name = summary['name']
        del summary['name']

        summary['id'] = hero_id
        heroes_summary[hero_name] = summary

    return heroes_summary


# hero is represented by tr tag which contains td tags inside - attributes
# span tags with id='tooltip' cointain column name and description as a title

def parse_table(heroes_summary):
    ''' Creates a list of the dictionaries with heroes attributes.

        :Args:
            heroes_summary (dict): {hero_name: summary}, summary contain id.

        :Returns:
            heroes_table (list): list of dictionaries, each represents column
                                 in heroes_attr table.
    '''

    heroes_table = []

    # since I was blocke on gamepedia, I downloaded html page containing
    # heroes attributes table
    # FIXME: abspath here
    ap = '/Users/gasabr/AtoD/v2'
    filename = os.path.join(ap, 'heroes_table.html')

    with open(filename, 'r') as fp:
        bs = BeautifulSoup(fp, 'html.parser')
        tables = bs.find_all('table')

        heroes = tables[1].findAll('tr')
        for hero in heroes[1:]:
            tds = hero.find_all('td')

            hero_dict = {}
            hero_dict['name'] = tds[0].span.a.attrs['title']

            # get id from heroes_summary
            hero_dict['id']   = heroes_summary[hero_dict['name']]['id']

            for column_name, value in zip(features_list, tds[1:]):
                hero_dict[column_name] = value.text[:-1]

            heroes_table.append(hero_dict)

    return heroes_table


def get_heroes_list():
    ''' Wrapper function for parse_table(). '''
    hs = create_heroes_summary()
    heroes_table = parse_table(hs)

    return heroes_table


if __name__ == '__main__':
    get_heroes_list()
