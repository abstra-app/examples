from abstra.forms import *
from abstra import *
from datetime import datetime
from abstra.tables import run, insert

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
        .read_dropdown("Currency", currencies, key="currency")
        .read("Customer", key="customer")
        .read_dropdown("Legal entity", entities, key="legal_entity")
        .read_date("Receivable date", key="receivable_date")
        .run("Send")
    )

    return receivables


receivable = get_receivable()

insert(
    "receivables",
    {
        "description": receivable["description"],
        "amount": float(receivable["amount"]),
        "currency": receivable["currency"],
        "customer": receivable["customer"],
        "legal_entity": receivable["legal_entity"],
        "receivable_date": preprocessing_date(receivable["receivable_date"]),
    },
)

display("All clear, boss. Receivable added to your database.", button_text="👍")
