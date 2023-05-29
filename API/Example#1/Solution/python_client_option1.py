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
SID = 'XXXXXXX'

# The result of this exercise will be stored in this variable
COLLECTED_IOCS = dict()

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY))


# Option 1: Get IOCs for the submission summary API
# client.submission.summary --> /api/v4/submission/summary/sid/
for tag_name, tag_values in client.submission.summary(SID)['tags']['ioc'].items():
    for tag_value, tag_verdict, is_tag_safelisted in tag_values:
        # Check if verdict is indeed malicious
        if tag_name.startswith('network'):
            # Create the tag category if does not exist
            COLLECTED_IOCS.setdefault(tag_name, [])

            # Add the IOC to our list of collected IOCs
            COLLECTED_IOCS['tag_name'].append(tag_value)

# Option 2: Get IOCs from the ontology API
# client.ontology.submission --> /api/v4/ontology/submission/sid/


# Now that we have gathered the IOCs, let's print them to the screen
pprint(COLLECTED_IOCS)
