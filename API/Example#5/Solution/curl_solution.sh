#!/bin/bash
# Exercise #5: Ingest files through Ingest/Submit API using CURL

export AL_HOST=localhost
export AL_USER=admin
export AL_APIKEY=devkey:admin

# CURL cheat sheet
#  to pass headers: -H 'key: value'
#  to set the request type: -X GET
#  to stop cert validation: -k
#  to add a file as a multipart:
#        -F 'name=data'
#        -F 'name=@path_to_file'

# Ingest / Submit API cheatsheet
#   * JSON parameters to the submission are passed inside a multipart object named 'json'
#   * The file binary is passed inside a multipart object named 'bin'

# ** Tip: you can pipe the curl output to json_pp so you can actually read it


# Send a file for asynchronous processing using CURL
# ** API to use: /api/v4/ingest/ (POST)
echo "Send to ingest API:"
curl -s -k -X POST https://$AL_HOST/api/v4/ingest/ \
    -H "x-user: ${AL_USER}" \
    -H "x-apikey: ${AL_APIKEY}" \
    -H 'accept: application/json' \
    -F 'json={"params": {"description": "My CURL test"}, "metadata": {"any_key": "any_value"}}' \
    -F 'bin=@myfile.txt' | json_pp

# Send a file for live processing using CURL
# ** API to use: /api/v4/submit/
echo ""
echo "Send to submit API:"
curl -s -k -X POST https://$AL_HOST/api/v4/submit/ \
    -H "x-user: ${AL_USER}" \
    -H "x-apikey: ${AL_APIKEY}" \
    -H 'accept: application/json' \
    -F 'json={"params": {"description": "My CURL test"}, "metadata": {"any_key": "any_value"}}' \
    -F 'bin=@myfile.txt' | json_pp
