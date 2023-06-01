# Exercise #2: Performing Filtered File Collection

# Download all files from assemblyline that scored over 2000 and
# store these files as cart so they don't trigger AV

import requests
import os

headers = {
    "x-user": os.getenv('AL_USER', 'first'),
    "x-apikey": os.getenv('AL_APIKEY', 'RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6'),
    "accept": "application/json"
}

# Filter for files within a submission that exceed a certain score
FILE_SCORE_THRESHOLD = 8000

# Download files that meet the FILE_SCORE_THRESHOLD into this directory
OUTPUT_DIRECTORY = '/tmp/ex2'
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# This is the connection to the Assemblyline client that we will use
host = f"https://{os.getenv('AL_HOST', 'ec2-3-98-100-58.ca-central-1.compute.amazonaws.com')}:443"

# For all submissions that are over the file score threshold
# client.search.stream.submission --> /api/v4/search/submission/
# ** NOTE: this works for the purpose of this demo but in real life you'd have to
#          keep track of the deep_paging_id in a while loop.
data = requests.get(f"{host}/api/v4/search/submission/?fl=sid&query=max_score:>={FILE_SCORE_THRESHOLD}",
                    headers=headers, verify=False).json()['api_response']['items']

for submission in data:
    # Download the full submission result and compute the score for each file
    # client.submission.full --> /api/v4/submission/full/sid/
    submission_results = requests.get(f"{host}/api/v4/submission/full/{submission['sid']}/",
                                      headers=headers, verify=False).json()['api_response']

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
            with open(os.path.join(OUTPUT_DIRECTORY, f"{sha256}.cart"), 'wb') as file:
                raw_file = requests.get(f"{host}/api/v4/file/download/{sha256}/?encoding=cart",
                                        headers=headers, verify=False).content
                file.write(raw_file)
