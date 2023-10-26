from abstra.workflows import get_stage
from os import getenv
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

stage = get_stage()


def get_stocks():
    url = "https://twelve-data1.p.rapidapi.com/stocks"

    querystring = {"exchange": "NASDAQ", "format": "json"}

    headers = {
        "X-RapidAPI-Key": getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": getenv("RAPIDAPI_HOST"),
    }

    stocks_raw = requests.get(url, headers=headers, params=querystring)

    stocks = stocks_raw.json()
    df = pd.DataFrame(stocks["data"])

    return df


df = get_stocks()
stage["stocks_df"] = df.to_dict()
