#Exercise #1 : Collecting IOCs

from assemblyline_client import get_client
# Connect/Authenticate with Assemblyline deployment
#PORT = '443'
#client = get_client('https://localhost:%s' % PORT, auth=('admin', 'admin'), verify=False)

from dotenv import dotenv_values
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values("ENV.env")
client = get_client("https://%s:443" % config["DOMAIN_STG"], apikey=(config["USERNAME"], config["KEY_STG"]))

# Pull IOCs from submission (without Ontology API)

# Store IOCs in variables that can be used to dump to disk to sent to another process
SUB_COLLECTED_IOCS, ONT_COLLECTED_IOCS = dict(), dict()

# Grab the first most recent completed submission
sid = client.search.submission(query="state:completed", fl='sid', rows=1, sort="times.completed desc")['items'][0]['sid']

# Let's say we're only interested in gathering network IOC tags
for tag_name, tag_values in client.submission.summary(sid)['tags']['ioc'].items():
    for tag_value, tag_verdict, is_tag_safelisted in tag_values:
        # Check if verdict is indeed malicious
        if tag_name.startswith('network'):
            # Add the IOC to our list of collected IOCs
            SUB_COLLECTED_IOCS.setdefault(tag_name, []).append(tag_value)

# Pull IOCs from submission (with Ontology API)            
# Let's perform the same operation but with the Ontology API            
for record in client.ontology.submission(sid):
    for tag_name, tag_values in record['results']['tags'].items():
        if tag_name.startswith('network'):
            # Add the IOC to our list of collected IOCs
            ONT_COLLECTED_IOCS.setdefault(tag_name, []).extend(tag_values)