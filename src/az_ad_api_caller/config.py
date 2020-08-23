import os
config = {
    "authority": "https://login.microsoftonline.com/{}".format(os.environ.get('TENANT_ID')),
    "client_id": "{}".format(os.environ.get('APPLICATION_ID')),
    "scope": ["https://graph.microsoft.com/.default"],
    "secret": "{}".format(os.environ.get('APPLICATION_SECRET')),
    "service_principal_name": "{}".format(os.environ.get('SERVICE_PRINCIPAL_NAME')),
    "user_principal_name": "{}".format(os.environ.get('USER_PRINCIPAL_NAME')),
    "group_principal_name": "{}".format(os.environ.get('GROUP_PRINCIPAL_NAME')),
    "app_role_name": "{}".format(os.environ.get('APP_ROLE_NAME'))
}
