"""
With this form, you can register or update a customer's info straight into your db.

You can use any Postgres db with this example, just keep an eye out for small modifications and
adjust the example's field names according to your set up.

We've set up this form (and Abstra's ERP) using Tables, our Postgres db service.
"""

import os
from abstra.forms import *
from abstra import *
from datetime import datetime

# This form uses an environment variable. To make it work properly, add an API Key to your workspace's environment variables in the sidebar.
tables = Tables(api_key=os.environ.get("TABLES_ERP_TOKEN"))


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


def replace_empty_list(data):
    return tuple(map(lambda x: x if x else None, data))


def convert_db_to_dropdown_format(label, value, statement_id):
    dict = tables.run_statement(id=statement_id)
    for d in dict:
        d["label"] = d.pop(label)
        d["value"] = d.pop(value)
    return dict


registration = read_multiple_choice(
    "Hello! Before continuing, what would you like to do?",
    [
        {"label": "Register a new customer", "value": "first_time"},
        {"label": "Update a customer", "value": "update"},
    ],
)

if registration == "first_time":
    customer = (
        Page()
        .read("Name")
        .read_email("Email")
        .read_dropdown(
            "Legal entity",
            [
                {"label": "Physical", "value": "physical"},
                {"label": "Juridical", "value": "juridical"},
            ],
        )
        .read_dropdown("Payment Frequency", ["Monthly", "Annual"])
        .read_dropdown("Payment Method", ["Credit card", "Wire Transfer"])
        .read("Country")
        .read_date("Registration date")
        .run("Send")
    )

    (
        name,
        email,
        legal_entity,
        payment_frequency,
        payment_method,
        country,
        created_data,
    ) = customer.values()

    created_data = preprocessing_date(created_data)

    payment_frequency, payment_method = replace_empty_list(
        [payment_frequency, payment_method]
    )

    # Here you'll need to set your database's query statement in order to properly update it
    # We'll continue this example without doing so to keep the data stable

    # statement = tables.statement(id="your_statement_id")

    # result = statement.run(params={"name":name, "email":email, "legal_entity": legal_entity, "payment_frequency": payment_frequency,\
    #                                 "payment_method": payment_method,\
    #                                 "country": country, "created_at":created_data})

    display(
        "Perfecto. Your new customer has been registered 😎",
        button_text="See you next time",
    )


else:
    customers = convert_db_to_dropdown_format(
        "name", "id", "f3bd4d41-e9f5-4cf2-926d-842f9eaa893f"
    )

    customer_id = read_dropdown("Which customer do you want to update data", customers)

    customer = (
        Page()
        .read("Name", required=False)
        .read_email("Email", required=False)
        .read_dropdown(
            "Legal entity",
            [
                {"label": "Physical", "value": "physical"},
                {"label": "Juridical", "value": "juridical"},
            ],
            required=False,
        )
        .read_dropdown("Payment Frequency", ["Monthly", "Annual"], required=False)
        .read_dropdown(
            "Payment Method", ["Credit card", "Wire Transfer"], required=False
        )
        .read("Country", required=False)
        .read_date("Churn date", required=False)
        .run("Send")
    )

    (
        name,
        email,
        legal_entity,
        payment_frequency,
        payment_method,
        country,
        churn_date,
    ) = customer.values()

    churn_date = preprocessing_date(churn_date)
    payment_frequency, payment_method = replace_empty_list(
        [payment_frequency, payment_method]
    )

    # Here you'll need to set your database's query statement in order to properly update it
    # We'll continue this example without doing so to keep the data stable

    # statement = tables.statement(id="your_statement_id")

    # result = statement.run(params={"customer_id": customer_id,"name":name, "email":email,\
    #                                "legal_entity": legal_entity,"payment_frequency": payment_frequency,\
    #                                "payment_method": payment_method,\
    #                                "country": country,  "churn_at":churn_date})

    display(
        "Great! The customer's data has been updated in your database.",
        button_text="See you next time",
    )
