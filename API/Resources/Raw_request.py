# Raw python request exercises
#Recommend to use the API Key.Otherwise, you will have to build yourself a library that will handle session cookies and XSRF tokens and you probably want something simpler.
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
    #CURL equivalent :curl -X POST -d json_dict -F json_file -H  header_string https://endpoint/api/v4/ingest/
    return API_request(method="POST",resource_path="/api/v4/ingest/",body=data,headers=headers,files=files)