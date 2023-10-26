### Check out the tutorial on how to set up your Sheets connection:
### https://www.abstracloud.com/tutorials/python-spreadsheet-integration


from abstra.hooks import get_request, send_json
import os

body, query, headers = get_request()


if headers["Api-Key"] != os.environ["API_KEY"]:
    send_json(data={"ok": False}, status_code=403)
else:
    values = body["values"]
    name = values[1]
    email = values[2]
    className = values[3]

    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Class: {className}")

    send_json(data={"received": values}, status_code=200)
