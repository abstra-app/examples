from abstra.forms import *
import requests
import json
from datetime import datetime
from datetime import date
import pandas as pd
from dateutil import relativedelta
import os

display("Hi! Welcome to our Invoice Factoring Calculator.",
        button_text="Let's get started")

id_assignor = read_multiple_choice("Please choose from the list of example assignors:",
                                   [{"label": "McQueen's Auto Shop", "value": 1},
                                    {"label": "Willy's Chocolate Factory", "value": 2},
                                       {"label": "Dexter's Lab Gear", "value": 3}]
                                   )

# This form uses an environment variable. To make it work properly, add an API Key to your workspace's environment variables in the sidebar.
key1 = os.environ['TABLES_INV_GET_ASSIGNOR_INFO']
# get assignor info from db
assignor = requests.post(
    f"https://tables.abstra.cloud/execute/{key1}",
    json={'id_assignor': int(id_assignor)}
)
assignor = assignor.json()[0]
assignor_name = assignor['name']
monthly_interest_rate = assignor['monthly_interest_rate']
monthly_interest_rate_display = str(monthly_interest_rate*100)+"%"
credit_limit = assignor['credit_limit']

# display assignor info as pandas table
data = {
    'Assignor Name': [assignor_name],
    'Monthly Interest Rate': [monthly_interest_rate_display]
}
df = pd.DataFrame(data)
blankIndex = [''] * len(df)
df.index = blankIndex
Page().display("Here are the receivables financing terms for this assignor.")\
      .display_pandas(df)\
      .run()

invoice = Page().display("Now, let's calculate terms for a new invoice.")\
                .read_number("What is the total value of this invoice?")\
                .read_date("When is this invoice due?")\
                .run()
invoice_value = invoice["What is the total value of this invoice?"]
invoice_due = invoice["When is this invoice due?"]

# calculate interest MoM
today = date.today()
end_date = datetime.strptime(str(invoice_due), '%Y-%m-%d')
today_date = datetime.strptime(str(today), '%Y-%m-%d')
r = relativedelta.relativedelta(end_date, today_date)

# check if enough credit in monthly credit limit

# This form uses an environment variable. To make it work properly, add an API Key to your workspace's environment variables in the sidebar.
key2 = os.environ['TABLES_INV_GET_SUPPLIER_INFO']

# get supplier list from db
suppliers = requests.post(
    f"https://tables.abstra.cloud/execute/{key2}").json()
chosen_supplier = read_dropdown(
    "Choose a supplier from this list to calculate risk multiplier.",
    options=[
        {'label': supplier['name'],
         'value':supplier['id']
         }
        for supplier in suppliers
    ]
)

# This form uses an environment variable. To make it work properly, add an API Key to your workspace's environment variables in the sidebar.
key3 = os.environ['TABLES_INF_GET_SUPPLIER_DETAILS']

# get supplier details from selection
new_supplier = requests.post(
    f"https://tables.abstra.cloud/execute/{key3}",
    json={'id_supplier': chosen_supplier}
)
new_supplier = new_supplier.json()[0]
risk_multiplier = str(new_supplier['risk_multiplier'])
# calculate new interest rate
new_interest_rate = monthly_interest_rate * float(risk_multiplier)
new_interest_rate_display = str(new_interest_rate*100)
display(f"OK! {new_supplier['name']} has a risk multiplier of {risk_multiplier} because they {new_supplier['notes']}. The new updated interest rate is {new_interest_rate_display}%.")

# calculate amount deductible
new_invoice_value = invoice_value - \
    (invoice_value * (new_interest_rate * r.months))

Page().display(f"The take rate for this invoice is calculated at {new_interest_rate_display}% over {r.months} months, given the invoice due date, assignor credit score and relevant supplier historical data.")\
      .display(f"The amount payable for this invoice is ${new_invoice_value}.")\
      .run("Finish")
