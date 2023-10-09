from abstra.forms import *
import os
import requests
import pandas as pd
from datetime import datetime, date, timezone
import json

ans = Page().display_markdown("""
## Hello! This form receives a list of Apollo contacts and populates them into your Hubspot Sales Pipeline.""")\
        .read_file("Just export an Apollo list with your leads as a .csv and upload it below:", key="contact_file")\
        .run()


# We had to comment the integrations due to API policy!
# Just paste into your own workspace and uncomment :)


# contact_file = ans["contact_file"]
# file = contact_file.file

# df = pd.read_csv(file)
# # Remove empty emails
# df_contacts = df.dropna(subset=['Email'])

# emails_list = df_contacts['Email'].tolist()

# def get_contacts_from_apollo(token, email):
#     url = "https://api.apollo.io/v1/contacts/search"
#     data = {
#         "api_key": token,
#         "q_keywords": email,
#         "sort_by_field": "contact_last_activity_date",
#         "sort_ascending": False,
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, json=data)
#     return response.json()


# create_deal_url = "https://api.hubapi.com/crm/v3/objects/deals"
# headers = {'Authorization': 'Bearer '+ hubspot_token,
#            'Content-Type': 'application/json'}


# for i in range(len(df_contacts)):
#     contact_email = df_contacts.loc[i, "Email"]
#     contact_data = get_contacts_from_apollo(apollo_token, contact_email)['contacts'][0]
#     contact = {'hubspot_vid': contact_data['hubspot_vid'],\
#                'first_name': contact_data['first_name'],\
#                'last_name': contact_data['last_name'],\
#                'company': contact_data['organization_name']}
#     print(contact) #add to list e display_pandas da tabela
#     if contact['last_name'] != None: 
#         last_name = contact['last_name']
#     else:
#         last_name = ''

#     today = datetime.today().strftime("%Y-%m-%d")
#     now = datetime.today().strftime("%Y-%m-%dT%H:%M:%S.Z")

#     hubspot_deal_stages = {
#         "prospected": "33921390", #Deal stage id
#         "mapped": "48862256" #Deal stage id
#     }

#     data = {
#     "properties": {
#         "became_mapped_date": today, #Customized Hubspot property from our deal pipeline
#         "became_prospected_date": today, #Customized Hubspot property from our deal pipeline
#         "closedate": now,
#         "dealname": contact['company'] + ' ' + '- ' + contact['first_name'] + ' ' + last_name,
#         "dealstage": hubspot_deal_stages["prospected"],
#         "hubspot_owner_id": "117155623", #Hubspot owner profile's id
#         "pipeline": "11412235" #Hubspot deal pipeline id
#     }}
    
#     deal_response = requests.post(create_deal_url, data=json.dumps(data), headers=headers)
#     deal_id = deal_response.json()['id']
#     df_contacts.loc[i, "Hubspot deal id"] = deal_id
#     df_contacts.loc[i, "Hubspot contact id"] = contact['hubspot_vid']

#     associate_deal_url = "https://api.hubapi.com/crm-associations/v1/associations"
#     headers = {'Authorization': 'Bearer '+ hubspot_token,
#                'Content-Type': 'application/json'}
#     data = {
#             "fromObjectId": contact['hubspot_vid'],
#             "toObjectId": deal_id,
#             "category": "HUBSPOT_DEFINED",
#             "definitionId": 4
#             }
#     associate_response = requests.put(associate_deal_url, data=json.dumps(data), headers=headers)
    
# dir_path =  "./apollo" 
# os.makedirs(dir_path, exist_ok=True)
# filename = datetime.today().strftime("%Y%m%d-%H-%M-%S") + "_deals.csv"
# df_contacts.to_csv(dir_path + '/' +filename)


display("Deals created! See you next time.")
