from assemblyline_client import get_client
# Connect/Authenticate with Assemblyline deployment
#PORT = '443'
#client = get_client('https://localhost:%s' % PORT, auth=('admin', 'admin'), verify=False)

from dotenv import dotenv_values
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values("ENV.env")
client = get_client("https://%s:443" % config["DOMAIN_STG"], apikey=(config["USERNAME"], config["KEY_STG"]))

def action_IOC(ioc: str): 
    print("I blocked %s!!!" %ioc)

# Let's say we want to inspect on IPs associated to 'suspicious' file submissions​

# Search through the alert index for items that match what we 're looking for​

# In the response, we only care to get the value of the IOC and its verdict​

for alert in client.search.alert('al.score:>500 AND al.ip:*', fl="al.detailed.ip.value,al.detailed.ip.verdict")['items']:
    # Iterate over the IPs in the alertl​
    for ioc in alert['al']['detailed']['ip']:
        # Ensure IOC isn't informational if we're going to action it​
        if ioc['verdict'] == 'info' :
            continue
        # Action this IOC (ie. add to FW rules)​
        action_IOC(ioc=ioc['value'])