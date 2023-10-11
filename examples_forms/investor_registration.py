from abstra.forms import *
from abstra.tables import run
from datetime import datetime


def add_investor(email, name, from_us, signature_date):
    sql = """
        INSERT INTO investors (email, name, from_us, signature_date)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
    """
    params = [
        email,
        name,
        from_us,
        signature_date,
    ]
    return run(sql, params)


def list_investors():
    sql = """
        SELECT id, email, name, from_us, signature_date FROM investors;
    """
    return run(sql)


def get_investor_data(investor_id):
    sql = """
        SELECT email, name, from_us, signature_date
        FROM investors
        WHERE id = $1;
    """
    params = [investor_id]
    return run(sql, params)[0]


def update_investor(email, name, from_us, signature_date, id):
    sql = """
        UPDATE investors
        SET email = $1, name = $2, from_us = $3, signature_date = $4
        WHERE id = $5;
    """
    params = [email, name, from_us, signature_date, id]
    return run(sql, params)


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


registration = read_multiple_choice(
    "Hello! What would you like to do?",
    [
        {"label": "Register a new investor", "value": "first_time"},
        {"label": "Update a investor", "value": "update"},
    ],
)

if registration == "first_time":
    investor = (
        Page()
        .read("name")
        .read_email("email")
        .read_multiple_choice(
            "From US?",
            [
                {"label": "yes", "value": "yes"},
                {"label": "no", "value": "no"},
            ],
        )
        .read_date("Signature date")
        .run("Send")
    )

    (name, email, from_us, signature_date) = investor.values()

    signature_date = preprocessing_date(signature_date)

    add_investor(email=email, name=name, from_us=from_us, signature_date=signature_date)

    display("New investor has been registered! See you later.")

else:
    investors_database = list_investors()

    investor = [
        {"label": f'{investor["name"]} ({investor["email"]})', "value": investor["id"]}
        for investor in investors_database
    ]

    investor_id = read_dropdown(
        "Which investor do you want to update data on?", investor
    )

    investor = get_investor_data(investor_id)

    updated_investor = (
        Page()
        .read("name", required=False)
        .read_email("email", required=False)
        .run("Send")
    )

    update_investor(
        email=updated_investor["email"] or investor["email"],
        name=updated_investor["name"] or investor["name"],
        from_us=investor["from_us"],
        signature_date=investor["signature_date"],
        id=investor_id,
    )
    display("Investor data has been updated! See you later.")
