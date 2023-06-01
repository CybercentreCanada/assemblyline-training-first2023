#!/bin/bash
# Exercise #5: Ingest files through Ingest/Submit API using CURL

export AL_HOST=ec2-15-223-69-3.ca-central-1.compute.amazonaws.com
export AL_USER=first
export AL_APIKEY=RW:60AAb)oviu!JgrD33pz3jpkX?hLY?CEw@AyYd(dMsv2qfEJ6

# CURL cheat sheet
#  to pass headers: -H 'key: value'
#  to set the request type: -X GET
#  to stop cert validation: -k
#  to add a multipart form data:
#        -F 'name=data'
#    OR  -F 'name=@path_to_file'

# Ingest / Submit API cheatsheet
#   * JSON parameters to the submission are passed inside a multipart object named 'json'
#   * The file binary is passed inside a multipart object named 'bin'

# ** Tip: you can pipe the curl output to json_pp so you can actually read it

# Send a file for asynchronous processing using CURL
# ** API to use: /api/v4/ingest/ (POST)


# Send a file for live processing using CURL
# ** API to use: /api/v4/submit/
