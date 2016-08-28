#!/usr/bin/env pyhton3

import openpyxl as xl
import json

import config

#___________________Reading data from xlsx____________________

# Open the workbook and select the first worksheet
wb = xl.load_workbook(config.features_file_xlsx)
sheet = wb.get_sheet_by_name('Sheet1')
 
# List to hold dictionaries
heroes = {}

xls_structure = {'A':'name', 'B':'id', 'C':'carry', 'D':'support', 'E':'nuker',
 'F':'disabler', 'G':'jungler', 'H':'durable', 'I':'escape', 'J':'pusher', 'K':'initiator', 
 'L':'range'}
 
# Iterate through each row in worksheet fetch values into dict
for rownum in range(2, sheet.max_row + 1):
    hero = {}
    # fetching values into dict
    for k, v in xls_structure.items():
        hero[v] = sheet[k + str(rownum)].value

    hero_id = hero.pop('id')
    heroes[hero_id] = hero

# Dumping to json
with open(config.features_file, 'w') as json_file:
    json.dump(heroes, json_file, indent=4)
