# Exercise #2: Performing Filtered File Collection

# Download all files from assemblyline that scored over 500 and
# store these files as cart so they don't trigger AV

import os
from assemblyline_client import get_client

AL_HOST = os.getenv('AL_HOST', 'localhost')
AL_USER = os.getenv('AL_USER', 'admin')
AL_APIKEY = os.getenv('AL_APIKEY', 'devkey:admin')

# Filter for files within a submission that exceed a certain score
FILE_SCORE_THRESHOLD = 2000

# Download files that meet the FILE_SCORE_THRESHOLD into this directory
OUTPUT_DIRECTORY = '/tmp/ex2'
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY), verify=False)

# For all submissions that are over the file score threshold
# client.search.stream.submission --> /api/v4/search/submission/?deep_paging_id=*
for record in client.search.stream.submission(query=f"max_score:>={FILE_SCORE_THRESHOLD}", fl='sid'):
    sid = record['sid']

    # Download the full submission result and compute the score for each file
    # client.submission.full --> /api/v4/submission/full/sid/
    submission_results = client.submission.full(sid)

    # Compute the score of each files in the submission
    files_scores = dict()
    for result in submission_results['results'].values():
        # Initialize the default score for the file if the file is not in the list
        files_scores.setdefault(result['sha256'], 0)

        # Add the score of the result record to the file
        files_scores[result['sha256']] += result['result']['score']

    # For each files where the score is greater than threshold, download in cARTed format
    # client.file.download --> /api/v4/file/download/sha256?encoding=cart/
    for sha256, score in files_scores.items():
        if score >= FILE_SCORE_THRESHOLD:
            client.file.download(sha256, encoding="cart", output=os.path.join(OUTPUT_DIRECTORY, f"{sha256}.cart"))
