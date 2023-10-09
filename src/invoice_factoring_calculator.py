from abstra.forms import *
from abstra.tables import run
from datetime import datetime
from datetime import date
import pandas as pd
from dateutil import relativedelta

display("Hi! Welcome to our Invoice Factoring Calculator.",
        button_text="Let's get started")

# Here we are selecting the assignor form our db: 

def get_assignor():
        sql = """SELECT name, monthly_interest_rate, credit_limit, supplier, notes,
                 FROM invoicecalculator 
                 WHERE id = $1"""

        return run(sql)[0]

assignors_db = get_assignor()

assignors = [
        {"label": f'{customer["name"]} ({customer["email"]})', "value": customer["id"]}
        for customer in assignors_db
    ] 

id_assignor = read_multiple_choice("Please choose from the list of example assignors:",
                                   [{"label": "McQueen's Auto Shop", "value": 1},
                                    {"label": "Willy's Chocolate Factory", "value": 2},
                                       {"label": "Dexter's Lab Gear", "value": 3}]
                                   )


if id_assignor == 1:   
    def get_assignor(id_assignor):
        sql = """SELECT name, monthly_interest_rate, credit_limit 
                 FROM invoicecalculator 
                 WHERE id = $1"""

        params= [id_assignor]
        return run(sql, params)[0] 

elif id_assignor == 2: 
    def get_assignor(id_assignor):
        sql = """SELECT name, monthly_interest_rate, credit_limit 
                 FROM invoicecalculator 
                 WHERE id = $1"""

        params= [id_assignor]
        return run(sql, params)[0]      

elif id_assignor == 3:
    def get_assignor(id_assignor):
        sql = """SELECT name, monthly_interest_rate, credit_limit 
                 FROM invoicecalculator 
                 WHERE id = 3"""

        params= [id_assignor]
        return run(sql, params)[0]
        

# get assignor info from db
assignor = get_assignor(id_assignor)
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

def table_supplier():
    sql = """SELECT id_supplier, name, notes, risk_multiplier 
             FROM Invoice_Calculator"""

    return run(sql)

suppliers = table_supplier()
chosen_supplier = read_dropdown(
    "Choose a supplier from this list to calculate risk multiplier.",
    options=[
        {'label': suppliers['name'],
         'value':suppliers['id'],
         }
         for suppliers in suppliers
    ]
)
value = chosen_supplier.value()

# This form uses an environment variable. To make it work properly, add an API Key to your workspace's environment variables in the sidebar.
def get_supplier(chosen_supplier):
    sql="""SELECT id, name, notes, risk_multiplier 
           FROM Invoice_Calculator
           WHERE id_supplier = value"""
    params = [chosen_supplier]
    return run(sql, params)[0]

new_supplier = get_supplier(chosen_supplier)
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
