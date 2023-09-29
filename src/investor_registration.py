from abstra.forms import *
from abstra.tables import run
from datetime import datetime


def add_investor(name, email, from_us, signature_date):
    sql = """
        INSERT INTO customers (name, email, from_us, signature_date)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
    """
    params = [
        name,
        email,
        from_us,
        signature_date,
    ]
    return run(sql, params)


def update_investor(name, email, from_us, signature_date, id):
    sql = """ 
        UPDATE investors
        SET name = $1, email = $2, from_us = $3, signature_date = $4,
        WHERE id = $5;
    """	
    params = [
        name,
        email,
        from_us,
        signature_date,
        id,
    ]
    return run(sql, params)

def investor_list():
    sql = """
        SELECT id, name, email FROM investors;
    """
    return run(sql)

investors_db = investor_list()
    
def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


def replace_empty_list(data):
    return tuple(map(lambda x: x if x else None, data))

    
registration = read_multiple_choice("Hello! What would you like to do?",\
[{"label": "Register a new investor", "value":"first_time"},\
{"label":"Update a investor", "value":"update"}])

if registration == "first_time":

    investor = Page().display("Hello! To register a new investor, please add the information required in the fields below:")\
                    .read("Name")\
                    .read_email("Email")\
                    .read_multiple_choice("From the US?",\
                                        [{"label": "Yes", "value":True},\
                                        {"label":"No", "value":False}])\
                    .read_date("Signature date")\
                    .run("Send")


    name, email, from_us, signature_date = investor.values()

    add_investor(name= name,
                 email=email,
                 from_us=from_us,
                 signature_date=signature_date)

    created_date = preprocessing_date(signature_date)

    display("New investor has been registered! See you later.")

else:
    investors_information = tables.run_statement(id="eed30b99-6673-4994-9d12-a75d4b7a76d6")
    investors_name = list(map(lambda x: x['name'], investors_information))
    
    investor_name = read_dropdown("Which investor do you want to update data on?", investors_name)

    investor = Page().read("Name", required=False)\
                    .read_email("Email", required=False)\
                    .run("Send")

    name, email = investor.values()

    # Here you'll need to set your database's query statement in order to properly update it
    # We'll continue this example without doing so to keep the data stable

    #statement = tables.statement(id="my_statement_id")

    #result = statement.run(params={"name":name, "email":email, "investor_name":investor_name})

    display("Investor data has been updated! See you later.")
