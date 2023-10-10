from abstra.forms import *
from abstra import *
from datetime import datetime
from abstra.tables import run, api

# Here you can add your company's authentication.
# user = get_user()

# if not user.email.endswith('@mycompany.com'):
# exit()


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


def get_receivable():
    entities = [
        {"label": "Physical", "value": "physical"},
        {"label": "Juridical", "value": "juridical"},
    ]
    currencies = [{"label": "USD", "value": "usd"}, {"label": "BRL", "value": "brl"}]
    receivables = (
        Page()
        .display("Hello. To insert a receivable, please fill in the information below:")
        .read("Description", key="description")
        .read_number("Amount", key="amount")
        .read_dropdown("Currency", currencies, key="")
        .read("Customer")
        .read_dropdown("Legal entity", entities)
        .read_date("Receivable date")
        .run("Send")
    )

    return receivables


def insert_receivables_db():
    receivable = get_receivable()
    sql = """
        INSERT INTO receivables (description, amount, currency, customer, legal_entity, receivable_date)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
    """
    params = [
        receivable["description"],
        float(receivable["amount"]),
        receivable["currency"],
        receivable["customer"],
        receivable["legal_entity"],
        preprocessing_date(receivable["receivable_date"]),
    ]
    return run(sql, params)


insert_receivables_db()
display("All clear, boss. Receivable added to your database.", button_text="👍")
