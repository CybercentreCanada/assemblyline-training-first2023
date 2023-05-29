#Exercise #2: Performing Filtered File Collection

#client.search.submission --> /api/v4/search/index/ --> curl -X POST -d json_dict -H  header_string_with_content https://endpoint/api/v4/search/index/
#client.submission.full --> /api/v4/submission/full/sid/ --> curl -H  header_string https://endpoint/api/v4/submission/full/sid/
#client.submission.file --> /api/v4/submission/sid/file/sha256/ --> curl -H  header_string https://endpoint/api/v4/submission/sid/file/sha256/
#client.file.download --> /api/v4/file/download/sha256?encoding=cart/ --> curl -H  header_string https://endpoint/api/v4/file/download/sha256?encoding=cart

import requests
import socket
import time
import json
import os
import urllib3
from dotenv import dotenv_values
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dict()
config["DOMAIN"] = "localhost" 
config["PORT"] = "443"
config["USERNAME"] = "admin"
config["KEY"] = "<key_name:randomly_generated_password>"

auth_header_with_content = {
    "x-user": config["USERNAME"],
    "x-apikey": config["KEY"],
    "accept": "application/json",
    "content-type": "application/json"
}
auth_header = {
    "x-user": config["USERNAME"],
    "x-apikey": config["KEY_STG"],
    "accept": "application/json",
}

def API_request(method,resource_path,body=None,headers=None,files=None):
    retry_counter = 0
    if method == "POST":
        while retry_counter < 5:
            try:
                response = requests.post('https://%s:%s%s' %(config["DOMAIN"],config["PORT"],resource_path),headers=headers,data=body,files=files,verify=False)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            except requests.exceptions.RequestException as err:
                raise SystemExit(err)
            except socket.error as error:
                print("Connection Failed due to socket - {}").format(error)
                print("Attempting %d of 5" % retry_counter)
                time.sleep(3)
                retry_counter  += 1
            else:
                return response
    elif method == "GET":
        while retry_counter < 5:
            try:
                response = requests.get('https://%s:%s%s' %(config["DOMAIN"],config["PORT"],resource_path),headers=headers,data=body,verify=False)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            except requests.exceptions.RequestException as err:
                raise SystemExit(err)
            except socket.error as error:
                print("Connection Failed due to socket - {}").format(error)
                print("Attempting %d of 5" % retry_counter)
                time.sleep(3)
                retry_counter  += 1
            else:
                return response
            
def search(index,query="",fields="id,score",rows=100,sort="field asc",headers=None):
    data = {
        "query": query,
        "offset": 0,  
        "rows": rows,
        "sort": sort,
        "fl": fields,
        "timeout": 1000,
        "filters": ['fq']
    }
    #CURL equivalent : curl -X POST -d json_dict -H  header_string https://endpoint/api/v4/search/%s/
    return API_request(method="POST",resource_path="/api/v4/search/%s/" % index,body=json.dumps(data),headers=headers)

# Download file(s) with a certain score

# Filter for submissions that exceed a certain score 
SUBMISSION_MAX_SCORE_MINIMUM = 1000
# Filter for files within a submission that exceed a certain score 
FILE_SCORE_THRESHOLD = 500 

# Grab a submission with certain overall max score
sid = search(index="submission",query=f"state:completed AND max_score:>{SUBMISSION_MAX_SCORE_MINIMUM}", fields='sid',rows=1,sort="times.completed desc",headers=auth_header_with_content).json()["api_response"]["items"][0]["sid"]
# Get the SHA256 of every file associated to the submission
#CURL equivalent :curl -H  header_string https://endpoint/api/v4/submission/full/%s/
full = API_request(method="GET",resource_path="/api/v4/submission/full/%s/" % sid,headers=auth_header).json()["api_response"]
for sha256 in list(full['file_infos'].keys()):
    # Compute the file's score relevant to the submission context
    file_score = 0
    #CURL equivalent :curl -H  header_string https://endpoint/api/v4/submission/%s/file/%s/
    file = API_request(method="GET",resource_path="/api/v4/submission/%s/file/%s/" % (sid,sha256),headers=auth_header).json()["api_response"]
    for result in file['results']:
        result = result['result']
        file_score += result['score']
        
    # If file score is greater than threshold, download in cARTed format
    if file_score >= FILE_SCORE_THRESHOLD:
        file = open('%s.cart' % sha256, 'wb')
        #CURL equivalent :curl -H  header_string https://endpoint/api/v4/file/download/%s?encoding=cart
        raw_file = API_request(method="GET",resource_path="/api/v4/file/download/%s?encoding=cart" % sha256,headers=auth_header)
        file.write(raw_file)
        file.close()