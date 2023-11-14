"""
Data lakes are an incresingly popular and cost-effective data storage solution.
This example sends contact info from Hubspot's CRM to a data lake in S3.
With our scheduler, bring all your data together automatically.
"""

import json
import os
import boto3
from datetime import datetime, timedelta
import requests

# This form uses an environment variable. To make it work properly, add a Hubspot API Key to your workspace's environment variables in the sidebar.
token = os.environ.get("HUBSPOT_TOKEN")

bucket_name = 'data-lake-raw-data'
contacts_filename = datetime.today().strftime('%Y-%m-%d') + \
    "_hubspot_contacts.json"


# get properties_name
properties_url = "https://api.hubapi.com/crm/v3/properties/contacts?archived=false&hapikey=" + token

try:
    properties_response = requests.get(properties_url)
    properties_name = [
        *map(lambda x: x["name"], properties_response.json()["results"])]
    properties_type = [
        *map(lambda x: x["type"], properties_response.json()["results"])]
except:
    print("Error {}".format(properties_response.status_code))


# get contact properties
contacts_url = "https://api.hubapi.com/crm/v3/objects/contacts/search?hapikey=" + token
headers = {"Content-Type": "application/json"}
time_to_get_contact = int(
    (datetime.now() - timedelta(days=1)).timestamp())  # in miliseconds
initial_time_to_get_contact = int(
    (datetime.now() - timedelta(days=360)).timestamp())
filter_group = [
    {
        "filters": [
            {
                "value": time_to_get_contact,
                "propertyName": "createdate",
                "operator": "GTE"
            }
        ]
    }
]


contacts_result = []
after = 0
while True:
    data = {
        "filterGroups": filter_group,
        "properties": properties_name,
        "limit": 100,
        "after": after
    }
    try:
        contacts_response = requests.post(
            contacts_url, data=json.dumps(data), headers=headers)
        contacts_result.extend(
            [*map(lambda x: x["properties"], contacts_response.json()["results"])])
        # print(contacts_response.json())

        if "paging" not in contacts_response.json():
            break
        after = contacts_response.json()["paging"]["next"]["after"]
    except:
        print("Error {}".format(properties_response.status_code))

with open(contacts_filename, 'w') as outfile:
    for x in contacts_result:
        json.dump(x, outfile)
        outfile.write('\n')


# Save files
def upload_to_aws(bucket_name, folder_name, s3_file):
    s3 = boto3.resource('s3',
                        # This form uses an environment variable. To make it work properly, add a AWS API Key to your workspace's environment variables in the sidebar.
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                        region_name='us-east-1')

    try:
        s3.Bucket(bucket_name).upload_file(
            s3_file, ("hubspot/" + folder_name + "/" + s3_file))
        return None
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None


s3_contacts = upload_to_aws(bucket_name, "contacts", contacts_filename)