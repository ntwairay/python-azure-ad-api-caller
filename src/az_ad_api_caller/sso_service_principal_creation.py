import sys  # For simplicity, we'll read config file from 1st CLI param sys.argv[1]
import json
import logging
# Optional logging
logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for entire script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs
import requests
from config import config
from authentication import authentication


def sso_service_principal_creation ():

    result = authentication()
    # configure headers
    headers                   = {'Authorization': 'Bearer ' + result['access_token']}
    headers['Content-Type']   = 'application/json'

    # Calling graph to create service principal with SSO using the access token
    sp_data =  {
        "displayName": config['service_principal_name']
    }
    # This is the default application template recommanded by MS
    template_id   = "8adf8e6e-67b2-4cf2-a259-e3dc5476c621"
    sp_endpoint   = "https://graph.microsoft.com/beta/applicationTemplates/{}/instantiate".format(template_id)
    sp_graph_data = requests.post(
        sp_endpoint,
        headers=headers,
        data=json.dumps(sp_data))
    logging.info(sp_graph_data.json())


if __name__ == '__main__':
    sso_service_principal_creation()
