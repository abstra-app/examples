from abstra.forms import *
import requests

response = requests.post(url="https://hooks.abstra.cloud/examples/mock-api")

error_messages = {
    403: "Your request was not authorized. Please speak to your manager.",
    404: "The resource was not found. Try another one.",
    503: "This service is currently unavailable. Please try again later.",
}

data = response.json()

if response.status_code == 200:
    display_markdown(f"""# Successful request\n\n`{data}`""")
else:
    message = error_messages.get(response.status_code)
    server_error = data.get("error")
    display_markdown(
        f"""# Error
Server message: **{server_error}**\n\n
{message}"""
    )
