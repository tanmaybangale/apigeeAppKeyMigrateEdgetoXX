import requests
import json


# Apigee Configuration
APIGEE_ORG_NAME = "gdc-mig-tool-1"
APIGEE_BASE_URL = "https://api.enterprise.apigee.com/v1" 
APIGEE_X_TOKEN = "YOUR GCP APIGEE X TOKEN"
APIGEE_EDGE_TOKEN = "YOUR GCP APIGEE Edge TOKEN"



# Create API Key
def create_api_key(productList,attributesList,key,secret,expiresAt,issuedAt,scopes,status,expiresInSeconds,developer_email,app_name):
    key_request_body = json.dumps({
                    "apiProducts": productList,
                    "attributes": attributesList,
                    "consumerKey": key,
                    "consumerSecret": secret,
                    "expiresAt": expiresAt,
                    "issuedAt": issuedAt,
                    "scopes": scopes,
                    "status": status,
                    "expiresInSeconds": expiresInSeconds
                    })

    url = f"https://apigee.googleapis.com/v1/organizations/apg-hub-00/developers/{developer_email}/apps/{app_name}/keys"
    headers = {
    'Authorization': 'Bearer {APIGEE_X_TOKEN}'}
    
    response = requests.request("POST", url, headers=headers, data=key_request_body)
    return response

def fetch_listofDevelopers():
    url = f"{APIGEE_BASE_URL}/organizations/{APIGEE_ORG_NAME}/developers"
    headers = {
    'Authorization': 'Bearer {APIGEE_EDGE_TOKEN}'}
    
    response = requests.request("GET", url, headers=headers, data={})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching list of developers: {response.status_code} - {response.text}")

def fetch_developerApps(developer_mail):
    url = f"{APIGEE_BASE_URL}/organizations/{APIGEE_ORG_NAME}/developers/{developer_mail}"
    headers = {
     'Authorization': 'Bearer {APIGEE_EDGE_TOKEN}'
     }
    
    response = requests.request("GET", url, headers=headers, data={})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching apps of developer: {response.status_code} - {response.text}")

def fetch_developerAppInfo(developer_mail,appname):
    url = f"{APIGEE_BASE_URL}/organizations/{APIGEE_ORG_NAME}/developers/{developer_mail}/apps/{appname}"
    headers = {
     'Authorization': 'Bearer {APIGEE_EDGE_TOKEN}'
     }
    
    response = requests.request("GET", url, headers=headers, data={})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching app info for the app of developers: {response.status_code} - {response.text}")

def updateDeveloperAppKey(developer_email,app_name,key,productList,status):
    
    key_request_body = json.dumps({
                    "apiProducts": productList
                    })

    url = f"https://apigee.googleapis.com/v1/organizations/apg-hub-00/developers/{developer_email}/apps/{app_name}/keys/{key}?action={status}"
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {APIGEE_X_TOKEN}'
     }
    
    print(key_request_body)
    response = requests.request("POST", url, headers=headers, data=key_request_body)
    return response


# Main Execution
if __name__ == "__main__":
    try:
        developerlist = fetch_listofDevelopers()
        for developer in developerlist:
            apps_list = fetch_developerApps(developer)
            for app in apps_list["apps"]:
                app_info = fetch_developerAppInfo(developer,app)
                appname = app_info['name']
                developermail = developer
                for cred in app_info['credentials'] :
                    productList = [ product['apiproduct'] for product in cred["apiProducts"]]
                    attributesList = cred["attributes"]
                    key = cred['consumerKey']
                    secret = cred['consumerSecret']
                    expiresAt = cred['expiresAt']
                    issuedAt = cred['issuedAt']
                    scopes = cred['scopes']
                    status = cred['status']

                    print(f"Creating API key for app: {appname} (Developer: {developermail}) key : {key}")
                    
                    #new_key_response = app_info['credentials']
                    create_api_key_response = create_api_key(productList,attributesList,key,secret,expiresAt,issuedAt,scopes,status,"-1",developermail,appname)
                
                    print(f"New API Key Created: {appname} , {create_api_key_response}") 
                    
                    product_added_response = updateDeveloperAppKey(developermail,appname,key,productList,status)
                    print(f"productlist added in : {appname} creds :{key} , {product_added_response}") 

    except Exception as e:
        print(f"An error occurred: {e}")