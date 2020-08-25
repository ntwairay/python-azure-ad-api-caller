# Azure AD API Callers

The purpose of this repository is to fill in the gap that is exisiting in Terraform Azure AD provider. At the moment, the provider does not provide
a way to allow role assignment to user and group in Enterprise Application (Service principal) and this could become a bit blocker for the team when
they are trying to automate the entire Azure AD process. Furthermore, it is also encountring some issue on creating Azure Enterprise Application (Service pricinipal)
with Single Sign On enable due to graph api issue. Therefore this repository will be the work around method until the provider is ready.

## Components ##
- Python
- requests
- msal

## Prerequisite ##
- python3 -m venv env
- . env/bin/activate
- pip3 install -r requirements.txt

## API permission of the Application (Delegated) ##

| Permission type             | Permissions (from least to most privileged)                                                                 |
| --------------------------- |:-----------------------------------------------------------------------------:|
| Delegated (work or school account)	     | User.ReadWrite.All                |
| Delegated (work or school account)	     | Group.ReadWrite.All               |
| Delegated (work or school account)       | Application.ReadWrite.All         |
| Delegated (work or school account)       | AppRoleAssignment.ReadWrite.All   |


## API permission of the Application (Application) ##
User.ReadWrite.All, Directory.ReadWrite.All
| Permission type             | Permissions (from least to most privileged)                                                                 |
| --------------------------- |:-----------------------------------------------------------------------------:|
| Application	                | User.ReadWrite.All                |
| Application	                | Group.ReadWrite.All               |
| Application                 | AppRoleAssignment.ReadWrite.All   |
| Application                 | Application.ReadWrite.All         |

## Quick start
### App role assignment
1. Export the environnment variables which are in env.sh.tpl
***example***
```
export TENANT_ID='1256789-ab-cd-ed'    (The tenant id of your application (Application Registeration)
export APPLICATION_ID='9999999999999'  (The application/client id of your application which will be used to access to graph api)     
export APPLICATION_SECRET='xxxxxxxxxxx'(The application/client secret of your application which you should have created under certificates and secrets )    
export SERVICE_PRINCIPAL_NAME='EXAMPLE-TEST'   (The name of your service principal which will contain the role assignment)
export USER_PRINCIPAL_NAME='ray.ng@example.com'(The user principal name of the user which will be assigned to the role)     
export APP_ROLE_NAME='Platform-team'           (The app role that you have created inside the manifest of the Service principal "EXAMPLE-TEST" under App Registeration)
export GROUP_PRINCIPAL_NAME='Internal-Platform-team' (The group principal name of the user which will be assigned to the role)
```

1. Execute app_role_assignment script to assigne the role to the user or group

```
python app_role_assignment.py add
```

1. Execute app_role_assignment script to delete the role to the user or group

```
python app_role_assignment.py delete
```

### SOO service principal creation
 1. Export the environnment variables which are in env.sh.tpl
 ***example***
 ```
 export TENANT_ID='1256789-ab-cd-ed'    (The tenant id of your application (Application Registeration)
 export APPLICATION_ID='9999999999999'  (The application/client id of your application which will be used to access to graph api)     
 export APPLICATION_SECRET='xxxxxxxxxxx'(The application/client secret of your application which you should have created under certificates and secrets )    
 export SERVICE_PRINCIPAL_NAME='EXAMPLE-TEST'   (The name of your service principal which will be created)
 ```

 1. Execute sso_service_principal_creation script to create the service principal
 ```
 python enterpise_application_creation.py
 ```
