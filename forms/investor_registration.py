from abstra.forms import *
from abstra.tables import run, insert, update
from datetime import datetime


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

    insert(
        "investors",
        {
            "email": email,
            "name": name,
            "from_us": from_us,
            "signature_date": signature_date,
        },
    )

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
        .read_multiple_choice(
            "From US?",
            [
                {"label": "yes", "value": "yes"},
                {"label": "no", "value": "no"},
            ],
            required=False,
            key="from_us",
        )
        .read_date("Signature date", required=False, key="signature_date")
        .run("Send")
    )

    update(
        "investors",
        {
            "email": updated_investor["email"],
            "name": updated_investor["name"],
            "from_us": updated_investor["from_us"],
            "signature_date": preprocessing_date(updated_investor["signature_date"]),
        },
        {"id": investor_id},
    )
    display("Investor data has been updated! See you later.")
