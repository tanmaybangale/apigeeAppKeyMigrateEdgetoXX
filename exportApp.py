import requests

# Your Apigee credentials and details
org_name = 'your-org-name'
developer_email = 'developer@example.com'
app_name = 'your-app-name'
consumer_key = 'the-consumer-key-you-want-to-fetch'

# Apigee API endpoint (constructed using the provided details)
api_endpoint = f'https://api.enterprise.apigee.com/v1/organizations/{org_name}/developers/{developer_email}/apps/{app_name}/keys/{consumer_key}'

# Your Apigee authentication headers (replace with your actual credentials)
headers = {
    'Authorization': 'Basic base64encoded_username_and_password', 
}

# Make the GET request
response = requests.get(api_endpoint, headers=headers)

# Check the response status
if response.status_code == 200:
    key_details = response.json()
    print(key_details)  # Print the retrieved key details
else:
    print(f"Error fetching key details: {response.status_code} - {response.text}")
