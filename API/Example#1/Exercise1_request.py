# Exercise #1 : Collecting IOCs

# Expected result:
# {
#     “network.static.ip”: [“172.0.0.1”, ...]
#     “network.static.domain”: [“www.google.com”, ...]
#     ...
# }

import requests
import os
from pprint import pprint

headers = {
    "x-user": os.getenv('AL_USER', 'admin'),
    "x-apikey": os.getenv('AL_APIKEY', 'devkey:admin'),
    "accept": "application/json"
}

# This is the submission ID that we will use to pull IOCs from
SID = 'XXXXXXX'

# The result of this exercise will be stored in this variable
COLLECTED_IOCS = dict()

# This is the connection to the Assemblyline client that we will use
host = f"https://{os.getenv('AL_HOST', 'localhost')}:443"


# Option 1: Get IOCs for the submission summary API
# client.submission.summary --> /api/v4/submission/summary/<sid>/

# Option 2: Get IOCs from the ontology API
# client.ontology.submission --> /api/v4/ontology/submission/<sid>/


# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
