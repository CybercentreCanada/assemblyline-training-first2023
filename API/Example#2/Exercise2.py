# Exercise #2: Performing Filtered File Collection

# Download all files from assemblyline that scored over 2000 and
# store these files as cart so they don't trigger AV

import os
from assemblyline_client import get_client

AL_HOST = os.getenv('AL_HOST', 'ec2-15-223-69-3.ca-central-1.compute.amazonaws.com')
AL_USER = os.getenv('AL_USER', 'first')
AL_APIKEY = os.getenv('AL_APIKEY', 'RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6')

# Filter for files within a submission that exceed a certain score
FILE_SCORE_THRESHOLD = 8000

# Download files that meet the FILE_SCORE_THRESHOLD into this directory
OUTPUT_DIRECTORY = '/tmp/ex2'
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY), verify=False)

# For all submissions that are over the file score threshold
# client.search.stream.submission --> /api/v4/search/submission/?deep_paging_id=*

# Download the full submission result and compute the score for each file
# client.submission.full --> /api/v4/submission/full/sid/

# For each files where the score is greater than threshold, download in cARTed format
# client.file.download --> /api/v4/file/download/sha256?encoding=cart/
