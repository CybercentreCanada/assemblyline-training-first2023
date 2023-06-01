# Exercise #3: Receive submission messages from the previously sent submissions to the ingest API
#              and print the score for each files

import os
from time import sleep

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

# This is the queue that will be use to communicate between your sender and receiver process
# ** You should have changed it in your sender... make it the same here!
NOTIFICATION_QUEUE_NAME = "CHANGE_THIS"


# Receive completion messages from the notification queue
# client.ingest.get_message_list --> /api/v4/ingest/get_message_list/<NOTIFICATION_QUEUE_NAME>/
while len(files_to_scan) != 0:
    for result in client.ingest.get_message_list(NOTIFICATION_QUEUE_NAME):
        # This is the file we are receiveing result for
        current_file = result['submission']['metadata']['file_path']

        # For each completetion message, pull the result record to get the score
        submission = client.submission(result['submission']['sid'])

        # Print file score to screen
        print(current_file, "=", submission['max_score'])

        # Stop waiting for the file
        files_to_scan.remove(current_file)

    # Otherwise wait for more messages until we're finished
    sleep(1)
