"""
We use this script to send weekly KPIs from Metabase to our team's Slack channel.
Just paste it into Jobs and get the whole team updated on key metrics.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from slack_sdk import WebClient
from dotenv import load_dotenv

# get environment variables
load_dotenv()

# This form uses an environment variable. To make it work properly, add a Metabase API Key to your workspace's environment variables in the sidebar.
metabase_token = os.environ.get("METABASE_TOKEN")

res = requests.post('https://metabase.YOUR_ENDPOINT/api/card/1/query/json',
                    headers={'Content-Type': 'application/json',
                             'X-Metabase-Session': metabase_token
                             }
                    )

df = pd.DataFrame(res.json())

week = datetime.today() - timedelta(days=7)

df_datetime = pd.to_datetime(df['Signup date'], format='%Y-%m-%d')

df_week = df[df_datetime > week]

message = pd.DataFrame.to_markdown(df_week)

# send to Slack

# This form uses an environment variable. To make it work properly, add a Slack API Key to your workspace's environment variables in the sidebar.
slack_token = os.environ.get("SLACK_TOKEN")
client = WebClient(token=slack_token)

client.chat_postMessage(
        channel="sa_planos",
        text=f"New users this week:\n {message}",
    )