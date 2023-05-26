#Exercise #2: Performing Filtered File Collection

from assemblyline_client import get_client
# Connect/Authenticate with Assemblyline deployment
#PORT = '443'
#client = get_client('https://localhost:%s' % PORT, auth=('admin', 'admin'), verify=False)

from dotenv import dotenv_values
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values("ENV.env")
client = get_client("https://%s:443" % config["DOMAIN_STG"], apikey=(config["USERNAME"], config["KEY_STG"]))

# Download file(s) with a certain score

# Filter for submissions that exceed a certain score 
SUBMISSION_MAX_SCORE_MINIMUM = 1000 
# Filter for files within a submission that exceed a certain score 
FILE_SCORE_THRESHOLD = 500 
# Download files that meet the FILE_SCORE_THRESHOLD into this directory
OUTPUT_DIRECTORY = '/tmp/'

# Grab a submission with certain overall max score
sid = client.search.submission(query=f"state:completed AND max_score:>{SUBMISSION_MAX_SCORE_MINIMUM}", fl='sid', rows=1, sort="times.completed desc")['items'][0]['sid']

# Get the SHA256 of every file associated to the submission
for sha256 in list(client.submission.full(sid)['file_infos'].keys()):
    # Compute the file's score relevant to the submission context
    file_score = 0
    for result in client.submission.file(sid, sha256)['results']:
        result = result['result']
        file_score += result['score']
        
    # If file score is greater than threshold, download in cARTed format
    if file_score >= FILE_SCORE_THRESHOLD:
        client.file.download(sha256, format="cart", output=os.path.join(OUTPUT_DIRECTORY, f"{sha256}.cart"))