''' Yet another abstraction. 

I did not know where to put initialisation of API, so here it is.
'''
import dota2api
from YamJam import yamjam

# this is just the way to access secret files in public projects
# fill free to replace the right part with your API key or
# learn how to use YamJam here: http://yamjam.readthedocs.io/en/v0.1.7/
DOTA_API_KEY = yamjam()['AtoD']['DOTA2_API_KEY']

api = dota2api.Initialise(DOTA_API_KEY)
