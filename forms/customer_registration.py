"""
With this form, you can register or update a customer's info straight into your db.

You can use any Postgres db with this example, just keep an eye out for small modifications and
adjust the example's field names according to your set up.

We've set up this form (and Abstra's ERP) using Tables, our Postgres db service.
"""

from abstra.forms import *
from abstra.tables import run, insert, update
from datetime import datetime


def list_customers():
    sql = """
        SELECT id, name, email FROM customers;
    """
    return run(sql)


def get_customer_data(customer_id):
    sql = """
        SELECT name, email, legal_entity, payment_frequency, payment_method, country, churn_at
        FROM customers
        WHERE id = $1;
    """
    params = [customer_id]
    return run(sql, params)[0]


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


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
        churn_at,
    ) = customer.values()

    churn_at = preprocessing_date(churn_at)

    insert(
        "customers",
        {
            "name": name,
            "email": email,
            "legal_entity": legal_entity,
            "payment_frequency": payment_frequency,
            "payment_method": payment_method,
            "country": country,
            "churn_at": churn_at,
        },
    )

    display(
        "Perfecto. Your new customer has been registered 😎",
        button_text="See you next time",
    )

else:
    customers_database = list_customers()  # [{ id, name, email }]

    customers = [
        {"label": f'{customer["name"]} ({customer["email"]})', "value": customer["id"]}
        for customer in customers_database
    ]  # [{ label, value }]

    customer_id = read_dropdown("Which customer do you want to update data", customers)

    customer_data = get_customer_data(customer_id)

    updated_customer = (
        Page()
        .read("Name", required=False, initial_value=customer_data["name"], key="name")
        .read_email(
            "Email", required=False, initial_value=customer_data["email"], key="email"
        )
        .read_dropdown(
            "Legal entity",
            [
                {"label": "Physical", "value": "physical"},
                {"label": "Juridical", "value": "juridical"},
            ],
            required=False,
            key="legal_entity",
            initial_value=customer_data["legal_entity"],
        )
        .read_dropdown(
            "Payment Frequency",
            ["Monthly", "Annual"],
            required=False,
            initial_value=customer_data["payment_frequency"],
            key="payment_frequency",
        )
        .read_dropdown(
            "Payment Method",
            ["Credit card", "Wire Transfer"],
            required=False,
            initial_value=customer_data["payment_method"],
            key="payment_method",
        )
        .read(
            "Country",
            required=False,
            initial_value=customer_data["country"],
            key="country",
        )
        .read_date(
            "Churn date",
            required=False,
            initial_value=customer_data["churn_at"],
            key="churn_date",
        )
        .run("Send")
    )

    updated_customer["churn_date"] = preprocessing_date(updated_customer["churn_date"])

    update(
        "customers",
        {
            "name": updated_customer["name"],
            "email": updated_customer["email"],
            "legal_entity": updated_customer["legal_entity"],
            "payment_frequency": updated_customer["payment_frequency"],
            "payment_method": updated_customer["payment_method"],
            "country": updated_customer["country"],
            "churn_at": updated_customer["churn_date"],
        },
        {"id": customer_id},
    )

    display(
        "Great! The customer's data has been updated in your database.",
        button_text="See you next time",
    )
