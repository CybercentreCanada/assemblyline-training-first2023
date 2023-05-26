from assemblyline_client import get_client
# Connect/Authenticate with Assemblyline deployment
#PORT = '443'
#client = get_client('https://localhost:%s' % PORT, auth=('admin', 'admin'), verify=False)

from dotenv import dotenv_values
import urllib3
import os
from time import sleep
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values("ENV.env")
client = get_client("https://%s:443" % config["DOMAIN_STG"], apikey=(config["USERNAME"], config["KEY_STG"]))

# Ingest files through Ingest API with(/out) notification queues

# Files within this directory will be ingested to Assemblyline
INGEST_DIR = '/tmp/'
QUEUED_IDS = []
NOTIF_QUEUED_IDS = [] 
NOTIFICATION_QUEUE_NAME = "testing_queue"
# Submission parameters (Only submit to Extract & Safelist service)
submission_params = { 
    'classification' : 'TLP:W',     # classification
    'description' : 'Hello world',  # file description
    'deep_scan' : False,            # activate deep scan mode
    'priority' : 1000,              # queue priority (the higher the number, the higher the priority)
    'ignore_cache' : False,         # ignore system cache
    'services' : {
        'selected' : [ # selected service list (override user profile)
            'Extract',
            'Safelist'
        ],
        'resubmit' : [],            # resubmit to these services if file initially scores > 500
        'excluded': [],             # exclude these services
    },
    'service_spec': {               # provide a service parameter
        'Extract': {
            'password': 'password'
        }
    }
}

# Ingest all files in the INGEST_DIR to Assemblyline
for root, _, files in os.walk(INGEST_DIR):
    for file in files:
        fp = os.path.join(root, file) 
        try:
            # Without notification queue
            QUEUED_IDS.append(client.ingest(path=fp, params=submission_params)['ingest_id'])
            # With notification queue
            NOTIF_QUEUED_IDS.append(client.ingest(path=fp, params=submission_params, nq=NOTIFICATION_QUEUE_NAME)['ingest_id'])
        except:
            pass

# Convenience of a notification queue is that you don't have to hammer the APIs to get results specific to you
# There's a dedicated message queue for you, if used.
while NOTIF_QUEUED_IDS:
    for result in client.ingest.get_message_list(NOTIFICATION_QUEUE_NAME):
        # Parse results and remove ID from queue
        NOTIF_QUEUED_IDS.remove(result['ingest_id'])
    # Otherwise wait for more messages until we're finished
    sleep(1)

# Otherwise, we have to use the ingest_id to look for our submissions using the Search API (which is intensive) and gather the results
while QUEUED_IDS:
    remove_IDS = []
    for ingest_id in QUEUED_IDS:
        for submission in client.search.submission(query=f"metadata.ingest_id:{ingest_id}", fl='sid', rows=1)['items']:
            # Parse results and and queue ID to be removed after loop
            remove_IDS.append(ingest_id)
    [QUEUED_IDS.remove(id) for id in remove_IDS]
    sleep(1)
