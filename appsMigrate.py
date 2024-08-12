import google.auth
from googleapiclient.discovery import build

# Replace with your actual values
ORGANIZATION_NAME = "your-organization-name"
DEVELOPER_EMAIL = "developer@example.com"
APP_NAME = "your-app-name"

# Authenticate using your preferred method (e.g., service account, user credentials)
creds, _ = google.auth.default()

# Build the Apigee API client
service = build('apigee', 'v1', credentials=creds)

# Construct the API key request body
key_request_body = {
    "consumerKey": "", # Leave blank for Apigee to generate a key
    "consumerSecret": "", # Leave blank for Apigee to generate a secret
    "scopes": [], # Specify any required API product scopes
    "expiresInSeconds": -1 # Set to -1 for no expiration
    # Add other optional fields as needed (e.g., status, attributes)
}

# Make the API call
response = service.organizations().developers().apps().keys().create(
    parent=f"organizations/{ORGANIZATION_NAME}/developers/{DEVELOPER_EMAIL}/apps/{APP_NAME}",
    body=key_request_body
).execute()

# Print the response
print(response)