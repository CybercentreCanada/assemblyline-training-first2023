#Exercise #3: Ingest files through Ingest API

#client.ingest --> /api/v4/ingest/ --> curl -X POST -d json_dict -F json_file -H  header_string_with_multipart https://endpoint/api/v4/ingest
#client.ingest.get_message_list --> /api/v4/ingest/get_message_list/nq_name/ --> curl -H header_string https://endpoint/api/v4/ingest/get_message_list/nq_name/
#client.search.submission --> /api/v4/search/index/ --> curl -X POST -d json_dict -H  header_string https://endpoint/api/v4/search/index/

import requests
import socket
import time
import json
import os
import urllib3
from dotenv import dotenv_values
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#config = dotenv_values("ENV.env")
config = dict()
config["DOMAIN"] = "localhost" 
config["PORT"] = "443"
config["USERNAME"] = "admin"
config["KEY"] = "<key_name:randomly_generated_password>"
#All Assemblyline APIs are built around receiving and returning JSON data. Do not forget to set your Content-Type and Accept headers to "application/json" or you might encounter some issues.
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

auth_header_with_multipart = {
    "x-user": config["USERNAME"],
    "x-apikey": config["KEY_STG"],
    "accept": "application/json",
    "content-type": None
}
#All Assemblyline APIs end with a trailing forward slash "/". Make sure that the API URL has it at the end of the URL otherwise you may get a "Method not allowed" error and you'll have issues figuring out why.

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

def ingest(file_path,params,headers,metadata={},nq=None):
    files={'bin': open(file_path, 'rb')}
    data={'json': json.dumps({'params': params, 'metadata': metadata,"notification_queue": nq})}
    #CURL equivalent :curl -X POST -d json_dict -F json_file -H  header_string https://endpoint/api/v4/ingest
    return API_request(method="POST",resource_path="/api/v4/ingest/",body=data,headers=headers,files=files)

# Files within this directory will be ingested to Assemblyline
INGEST_DIR = '.'
QUEUED_IDS = []
NOTIF_QUEUED_IDS = [] 
NOTIFICATION_QUEUE_NAME = "testing_queue"
# Submission parameters (Only submit to Extract & Safelist service)
submission_params = { 
    'classification' : 'TLP:C',     # classification
    'description' : 'Hello world',  # file description
    'deep_scan' : False,            # activate deep scan mode
    'priority' : 1000,              # queue priority (the higher the number, the higher the priority)
    'ignore_cache' : False,         # ignore system cache
    'alert' : False,                # Don't create an alert if scoring > 500
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

metadata = {
    'my_metadata' : 'value',     # any metadata of your liking
    'my_metadata2' : 'value2'     # any metadata of your liking
}

# Ingest all files in the INGEST_DIR to Assemblyline
for root, _, files in os.walk(INGEST_DIR):
    for file in files:
        fp = os.path.join(root, file) 
        try:
            # Without notification queue
            id = ingest(file_path=fp,params=submission_params,headers=auth_header_with_multipart)["api_response"]['ingest_id']
            QUEUED_IDS.append(id)
            # With notification queue
            id = ingest(file_path=fp,params=submission_params,headers=auth_header_with_multipart,nq=NOTIFICATION_QUEUE_NAME)["api_response"]['ingest_id']
            NOTIF_QUEUED_IDS.append(id)
        except:
            pass

# Convenience of a notification queue is that you don't have to hammer the APIs to get results specific to you
# There's a dedicated message queue for you, if used.
while NOTIF_QUEUED_IDS:
    #CURL equivalent :curl -H header_string https://endpoint/api/v4/ingest/get_message_list/%s/
    message_list = API_request(method="GET",resource_path="/api/v4/ingest/get_message_list/%s/" % NOTIFICATION_QUEUE_NAME,headers=auth_header)["api_response"]
    for result in message_list:
        # Parse results and remove ID from queue
        NOTIF_QUEUED_IDS.remove(result['ingest_id'])
    # Otherwise wait for more messages until we're finished
    time.sleep(1)

# Otherwise, we have to use the ingest_id to look for our submissions using the Search API (which is intensive) and gather the results
while QUEUED_IDS:
    remove_IDS = []
    for ingest_id in QUEUED_IDS:
        submission = search(index="submission",query=f"metadata.ingest_id:{ingest_id}", fields='sid',rows=1,sort="times.completed desc",headers=auth_header_with_content).json()["api_response"]
        for submission in submission['items']:
            # Parse results and and queue ID to be removed after loop
            remove_IDS.append(ingest_id)
    [QUEUED_IDS.remove(id) for id in remove_IDS]
    time.sleep(1)