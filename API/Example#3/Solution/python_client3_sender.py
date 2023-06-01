# Exercise #3: Ingest files through Ingest API

import os
from assemblyline_client import get_client

AL_HOST = os.getenv('AL_HOST', 'ec2-15-223-69-3.ca-central-1.compute.amazonaws.com')
AL_USER = os.getenv('AL_USER', 'first')
AL_APIKEY = os.getenv('AL_APIKEY', 'RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6')

# Files within this directory will be ingested to Assemblyline
#  ** Let's just reuse the files from exercise 2
INGEST_DIR = '/tmp/ex2'
files_to_scan = list()
for root, _, files in os.walk(INGEST_DIR):
    for file in files:
        files_to_scan.append(os.path.join(root, file))

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY), verify=False)

# Submission parameters
#  ** NOTE: This is only provided as an example you should not to use it to get the user's default values.
#           It's just here to show you that you can alter any submission parameters
submission_params = {
    'classification': 'TLP:C',                                      # classification
    'description': "I don't wanna use the user's default values!",  # description
    'deep_scan': False,                                             # activate deep scan mode
    'priority': 1000,              # queue priority (the higher the number, the higher the priority)
    'ignore_cache': False,         # ignore system cache
    'services': {
        'selected': [              # selected service list (override user profile)
            'Extract',
            'Safelist'
        ]
    },
    'service_spec': {               # provide a service parameter
        'Extract': {
            'password': 'password'
        }
    }
}

# This is the queue that will be use to communicate between your sender and receiver process
# ** please make it usnique for you so you don't receive messages from others!
NOTIFICATION_QUEUE_NAME = "CHANGE_THIS"


# Ingest files through Ingest API with a notification queue
# ** NOTE: you should add the path of the file you just scaned to
#          the metadata so you can keep track of it
# client.ingest --> /api/v4/ingest/

# Ingest all files to scan in Assemblyline
for file_path in files_to_scan:
    # That's it, just need to send all files in... the receiver will pull the results
    client.ingest(path=file_path, metadata={'file_path': file_path}, nq=NOTIFICATION_QUEUE_NAME)
