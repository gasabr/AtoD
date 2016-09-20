#!/usr/bin/env python3

# from given time (string of characters) get all(or a lot)
# matches from the patch

import time
import calendar
import dota2api
import json

import config

unix_time = calendar.timegm(time.strptime('Jun 14, 2016 @ 00:00:00 UTC', 
				'%b %d, %Y @ %H:%M:%S UTC')) # time when 6.88 was released

first_match_id = 2459838799 # 25.06.16 - start point for searching
last_match_id = 2569610900 # the last game of the International

# for i in range(first_match_id, last_match_id)

unsuccessful_requests = 0
i = 6
flag = False

while not flag:
	try:
		test = config.api.get_match_details(first_match_id+i)
	except dota2api.src.exceptions.APIError as e:
		i += 1
		unsuccessful_requests += 1
		print(e)
	else:
		flag = True

print(json.dumps(test, indent=1))
print("#unsuccessful requests:", unsuccessful_requests)

