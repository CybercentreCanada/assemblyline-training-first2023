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

AL_HOST = os.getenv('AL_HOST', 'localhost')
AL_USER = os.getenv('AL_USER', 'admin')
AL_APIKEY = os.getenv('AL_APIKEY', 'devkey:admin')


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
for record in client.ontology.submission(SID):
    for tag_name, tag_values in record['results']['tags'].items():
        if tag_name.startswith('network'):
            # Create the tag category if does not exist
            COLLECTED_IOCS.setdefault(tag_name, [])

            # Add the IOC to our list of collected IOCs
            COLLECTED_IOCS[tag_name].extend(tag_values)

# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
