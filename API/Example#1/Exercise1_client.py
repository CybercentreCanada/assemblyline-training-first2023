# Exercise #1 : Collecting IOCs

# Expected result:
# {
#     “network.static.ip”: [“172.0.0.1”, ...]
#     “network.static.domain”: [“www.google.com”, ...]
#     ...
# }

import os
from pprint import pprint
from assemblyline_client import get_client

AL_HOST = os.getenv('AL_HOST', 'ec2-15-223-69-3.ca-central-1.compute.amazonaws.com')
AL_USER = os.getenv('AL_USER', 'first')
AL_APIKEY = os.getenv('AL_APIKEY', 'RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6')


# This is the submission ID that we will use to pull IOCs from
SID = '1nAXRc365frBiSXKg0qX0Q'

# The result of this exercise will be stored in this variable
COLLECTED_IOCS = dict()

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY), verify=False)


# Option 1: Get IOCs for the submission summary API
# client.submission.summary --> /api/v4/submission/summary/sid/


# Option 2: Get IOCs from the ontology API
# client.ontology.submission --> /api/v4/ontology/submission/sid/


# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
