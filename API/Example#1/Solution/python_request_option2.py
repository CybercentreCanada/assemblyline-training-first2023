# Exercise #1 : Collecting IOCs

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
ontology = requests.get(f"{host}/api/v4/ontology/submission/{SID}/", headers=headers).json()["api_response"]
for record in ontology:
    for tag_name, tag_values in record['results']['tags'].items():
        if tag_name.startswith('network'):
            # Create the tag category if does not exist
            COLLECTED_IOCS.setdefault(tag_name, [])

            # Add the IOC to our list of collected IOCs
            COLLECTED_IOCS.extend(tag_values)


# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
