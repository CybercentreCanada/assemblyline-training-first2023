#!/bin/bash
export $(cat ENV.env)

curl -X POST https://$DOMAIN_STG/api/v4/submit/ \
    -H 'x-user: $($USERNAME)' \
    -H 'x-apikey: $($KEY_STG)' \
    -H 'accept: application/json' \
    -F 'json={"params": {"description": "My CURL test"}, "metadata": {"any_key": "any_value"}}' \
    -F 'bin=@myfile.txt'

curl -X POST https://$DOMAIN_STG/api/v4/ingest/ \
    -H 'x-user: $($USERNAME)' \
    -H 'x-apikey: $($KEY_STG)' \
    -H 'accept: application/json' \
    -F 'json={"params": {"description": "My CURL test"}, "metadata": {"any_key": "any_value"}}' \
    -F 'bin=@myfile.txt'