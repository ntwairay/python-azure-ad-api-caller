import sys  # For simplicity, we'll read config file from 1st CLI param sys.argv[1]
import json
import logging
# Optional logging
logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for entire script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs
import requests
import msal
from config import config
from authentication import authentication


def app_role_assignment ():
    result = authentication()
    # Calling graph to get service principal object Id using the access token
    headers       = {'Authorization': 'Bearer ' + result['access_token']}
    sp_endpoint   = "https://graph.microsoft.com/v1.0/servicePrincipals?$filter=displayName eq '{}'".format(config['service_principal_name'])
    sp_graph_data = requests.get(  # Use token to call downstream service
        sp_endpoint,
        headers=headers,).json()
    sp_object_id = sp_graph_data['value'][0]['id']
    logging.info("Service principal object ID is {}".format(sp_object_id))

    headers['Content-Type'] = 'application/json'

    # Calling graph to get user object Id using the access token
    if config['user_principal_name']:
        user_endpoint           = "https://graph.microsoft.com/v1.0/users/{}".format(config['user_principal_name'])
        user_graph_data = requests.get(  # Use token to call downstream service
            user_endpoint,
            headers=headers,).json()
        user_object_id = user_graph_data['id']
        logging.info("User principal object ID is {}".format(user_object_id))

    # Calling graph to get group object Id using the access token
    if config['group_principal_name']:
        group_endpoint           = "https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{}'".format(config['group_principal_name'])
        group_graph_data = requests.get(  # Use token to call downstream service
            group_endpoint,
            headers=headers,).json()
        group_object_id = group_graph_data['value'][0]['id']
        logging.info("Group principal object ID is {}".format(group_object_id))

    # Calling graph to get approle object Id using the access token
    app_role_endpoint   = "https://graph.microsoft.com/v1.0/applications?$filter=displayName eq '{}'".format(config['service_principal_name'])
    app_role_graph_data = requests.get(  # Use token to call downstream service
        app_role_endpoint,
        headers=headers,).json()
    app_roles = app_role_graph_data['value'][0]['appRoles']
    app_role = [ar for ar in app_roles if ar['value'] == config['app_role_name']]
    app_role_id = app_role[0]['id']
    logging.info("App Role object ID is {}".format(app_role_id))

    # Calling graph to do approle assignment using the access token
    if group_object_id:
        principal_id = group_object_id
        which        = "groups"
    elif user_object_id:
        principal_id = user_object_id
        which        = "users"
    else:
        logging.error("Group and User object id is empty")

    app_role_assignment_endpoint = "https://graph.microsoft.com/v1.0/{}/{}/appRoleAssignments".format(which,principal_id)
    app_role_assignment_data =  {
      "principalId": principal_id,
      "resourceId": sp_object_id, # the ip inside the approle for each role
      "appRoleId": app_role_id
    }
    logging.info("App Role assignment details:")
    logging.info(app_role_assignment_data)
    ar_assignment_graph_data = requests.post(
        app_role_assignment_endpoint,
        headers=headers,
        data=json.dumps(app_role_assignment_data))
    ar_assignment_graph_data.raise_for_status()
    logging.info('AppRole assignment for is completed')


if __name__ == '__main__':
    app_role_assignment()
