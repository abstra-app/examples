from abstra.forms import *
from abstra.tables import run, insert
from datetime import datetime


display("Hi! Welcome to our Purchase Requester.", button_text="Let's get started")


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


title = read("What is the title of this expense?")

value = read_number("How much was this expense?")

recurring = read_multiple_choice(
    "Is this a monthly recurring expense?",
    ["yes", "no"],
)

id_department = read_multiple_choice(
    "To which department_name does this expense belong?",
    [
        {"label": "Marketing", "value": "marketing"},
        {"label": "Sales", "value": "sales"},
        # {"label": "Operations", "value": "Operations"},
        # {"label": "Product", "value": "Product"},
        # {"label": "Human Resources", "value": "Human Resources"},
        # {"label": "Engineering", "value": "Engineering"},
    ],
)


def list_expenses():
    sql = f"""
        SELECT {id_department} FROM departments_budgets;
    """
    return run(sql)


budget = list_expenses()[0][id_department]
new_budget = budget - value
print(type(new_budget))


def update_budget():
    sql = f"""
        UPDATE departments_budgets
        SET {id_department} = $1
    """
    params = [new_budget]
    return run(sql, params)


# check if enough budget remains, if not jump to end
if value <= budget:
    description = read("Briefly describe what this expense is for.")
    type = read_multiple_choice(
        "What type of expense is this?", ["tool", "freelancer", "reimbursement", "misc"]
    )
    due = read_date("When is this expense due?")
    due = preprocessing_date(due)

    insert(
        "expenses",
        {
            "name": title,
            "description": description,
            "type": type,
            "value": value,
            "recurring_monthly": recurring,
            "due": due,
        },
    )

    update_budget()

    display("We've registered this expense succesfully. Thanks! See ya next time.")
else:
    display(
        f"Sorry, the budget for the {id_department} department_name is not sufficient to cover this expense. Please speak to your manager."
    )
