# Exercise #4: Alert monitoring and identify IOC for blocking

import os
from assemblyline_client import get_client

AL_HOST = os.getenv('AL_HOST', 'localhost')
AL_USER = os.getenv('AL_USER', 'admin')
AL_APIKEY = os.getenv('AL_APIKEY', 'devkey:admin')

# This is the connection to the Assemblyline client that we will use
client = get_client(f"https://{AL_HOST}:443", apikey=(AL_USER, AL_APIKEY), verify=False)


def block_IOC(ioc: str, ioc_type: str, verdict: str):
    # Fake block IOC function, this would obviously be tailored code for your systems
    print(f"Blocking {ioc_type.upper()}: {ioc} ({verdict})")


# Search through the alert index for alerts with IPs and Domains
# client.search.alert --> /api/v4/search/alert/

# Iterate over the IOCs in the alert

# Make sure those IOCs are not safe or informational

# Block suspicious and malicious IOCs (ie. add to FW rules)​
