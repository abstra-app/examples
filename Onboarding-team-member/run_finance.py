import os
import typing
import requests
from dotenv import load_dotenv

load_dotenv()

EXECUTE_URL = "https://cloud-api.abstra.cloud/cli/tables/execute"

# public api


def run_finance(query: str, params: typing.Optional[typing.List] = None):
    j_body = {"query": query, "params": params or []}

    headers = {
        "Content-Type": "application/json",
        "api-authorization": f"Bearer {os.getenv('FINANCE_AP_TOKEN')}",
    }

    if not os.getenv("FINANCE_AP_TOKEN"):
        raise Exception("You must be logged in to execute a tables query")

    r = requests.post(EXECUTE_URL, headers=headers, json=j_body)
    if not r.ok:
        raise Exception(f"Error executing query {query}: {r.text}")

    response = r.json()
    if response["errors"]:
        raise TablesExecutionError(response["errors"], query, params)

    return response["returns"]["result"]


class TablesExecutionError(Exception):  # public api
    def __init__(
        self,
        errors: typing.List,
        query: str,
        params: typing.Optional[typing.List] = None,
    ) -> None:
        self.query = query
        self.params = params
        self.errors = errors
