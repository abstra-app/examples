"""
This scripts is used in Abstra Cloud (https://abstracloud.com) to collect buying intentions.
This is a good example on how using Python scripts can be much simpler than forms + external automations
"""

from abstra.forms import *
from requests import post
import os

# This form uses an environment variable. To make it work properly, add a Slack API Key to your workspace's environment variables in the sidebar.
token = os.environ.get("SLACK_BOT_TOKEN")

if 'plan' in url_params:
    plan = url_params['plan']
else:
    plan = 'standard'

display("Thank you for showing interest in our " + plan +
        " plan. We need some informations to get in touch.")
name = read("Name")
email = read_email('Email')
company = read("Company name")

"""
This is the quickest way you can avoid sending messages
when someone on your company tests your script.
"""
# if '@abstra.app' not in email:
#     res = post(
#         'https://slack.com/api/chat.postMessage',
#         json={
#             'channel': 'sales',
#             'text': name + ' (' + email + ') wants to buy the ' + plan + ' plan'
#         },
#         headers={
#             'Authorization': 'Bearer ' + token,
#             'Content-type': 'application/json; charset=utf-8'
#         })

display("We've got your information, we'll get in contact soon! 😉")