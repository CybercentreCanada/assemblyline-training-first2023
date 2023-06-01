# Exercise #1 : Collecting IOCs

# Expected result:
# {
#     “network.static.ip”: [“172.0.0.1”, ...]
#     “network.static.domain”: [“www.google.com”, ...]
#     ...
# }

import requests
import json
import os
from pprint import pprint

headers = {
    "x-user": os.getenv('AL_USER', 'first'),
    "x-apikey": os.getenv('AL_APIKEY', 'RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6'),
    "accept": "application/json"
}

# This is the submission ID that we will use to pull IOCs from
SID = '1nAXRc365frBiSXKg0qX0Q'

# The result of this exercise will be stored in this variable
COLLECTED_IOCS = dict()

# This is the connection to the Assemblyline client that we will use
host = f"https://{os.getenv('AL_HOST', 'ec2-3-98-100-58.ca-central-1.compute.amazonaws.com')}:443"


# Option 1: Get IOCs for the submission summary API
# client.submission.summary --> /api/v4/submission/summary/<sid>/


# Option 2: Get IOCs from the ontology API
# client.ontology.submission --> /api/v4/ontology/submission/<sid>/


# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
