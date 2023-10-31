### Check out the tutorial on how to set up your Sheets connection:
### https://www.abstra.io/tutorials/python-spreadsheet-integration


from abstra.hooks import get_request, send_json
import os

body, query, headers = get_request()
list_values = []
for value in body.values():
    list_values.append(value)
print(list_values)
name = list_values[0]
email = list_values[1]
className = list_values[2]

print(f"Name: {name}")
print(f"Email: {email}")
print(f"Class: {className}")

send_json(data={"received": list_values}, status_code=200)
