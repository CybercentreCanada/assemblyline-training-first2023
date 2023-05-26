#Exercise #1 : Collecting IOCs

#client.search.submission --> /api/v4/search/index/ --> curl -X POST -d json_dict -H  header_string_with_content https://endpoint/api/v4/search/index/
#client.submission.summary --> /api/v4/submission/summary/sid/ --> curl -H  header_string https://endpoint/api/v4/submission/summary/sid/
#client.ontology.submission --> /api/v4/ontology/submission/sid/ --> curl -H  header_string https://endpoint/api/v4/ontology/submission/sid/

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

#Pulling a submission
sid = search(index="submission",query="state:completed", fields='sid',rows=1,sort="times.completed desc",headers=auth_header_with_content).json()["api_response"]["items"][0]["sid"]

# Pull IOCs from submission (without Ontology API)

# Store IOCs in variables that can be used to dump to disk to sent to another process
SUB_COLLECTED_IOCS, ONT_COLLECTED_IOCS = dict(), dict()
#CURL equivalent :curl -H  header_string https://endpoint/api/v4/submission/summary/%s/
summary = API_request(method="GET",resource_path="/api/v4/submission/summary/%s/" % sid,headers=auth_header).json()["api_response"]
for tag_name, tag_values in summary["tags"]["ioc"].items():
    for tag_value, tag_verdict, is_tag_safelisted in tag_values:
        # Check if verdict is indeed malicious
        if tag_name.startswith('network'):
            # Add the IOC to our list of collected IOCs
            SUB_COLLECTED_IOCS.setdefault(tag_name, []).append(tag_value)

# Pull IOCs from submission (with Ontology API)   
#          
# Let's perform the same operation but with the Ontology API
#CURL equivalent :curl -H  header_string https://endpoint/api/v4/ontology/submission/%s/
ontology = API_request(method="GET",resource_path="/api/v4/ontology/submission/%s/" % sid, headers=auth_header).json()
for record in ontology:
    for tag_name, tag_values in record['results']['tags'].items():
        if tag_name.startswith('network'):
            # Add the IOC to our list of collected IOCs
            ONT_COLLECTED_IOCS.setdefault(tag_name, []).extend(tag_values)