from assemblyline_client import get_client
# Connect/Authenticate with Assemblyline deployment
#PORT = '443'
#client = get_client('https://localhost:%s' % PORT, auth=('admin', 'admin'), verify=False)

from dotenv import dotenv_values
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = dotenv_values("ENV.env")
client = get_client("https://%s:443" % config["DOMAIN_STG"], apikey=(config["USERNAME"], config["KEY_STG"]))