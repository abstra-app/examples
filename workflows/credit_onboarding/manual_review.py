from abstra.forms import *
from abstra.workflows import get_data, set_data

display_markdown("""
<img src="https://abstracloud-webflow-assets.s3.amazonaws.com/7626icon.png" width="50" height="50" />

# CreditOps
### Loan request review 🔍
                 """, button_text="Start")


user = get_user()

if not user.email.endswith("abstra.io"):
    display("You don't have permission to access this review ❌")
    exit()

set_data("reviewing_user", user.email)

name = get_data("name")
email = get_data("email")
income = get_data("income")
employer = get_data("employer")
loan_amount = get_data("loan_amount")
installments = get_data("installments")
score = get_data("score")
reason_low_score = get_data("reason_low_score")


markdown_text = f"""
# Loan Request

----------------------------

## Personal Data

### Name: 
{name}
### Email: 
{email}

----------------------------

## Income Data

### Income: 
$ {income:,.2f}
### Employer: 
{employer}

----------------------------

## Loan Data

### Loan amount: 
$ {loan_amount:,.2f}
### Installments: 
{installments}

----------------------------

## Credit Engine Result

### Score: 
{score}
### Reason: 
{reason_low_score}

----------------------------
"""


selection = Page() \
    .display_markdown(markdown_text) \
    .read_multiple_choice("Do you want to approve this request?",["Yes", "No"], key="approval") \
    .run()

if selection['approval'] == "No":
    rejection_reason = read_textarea("Rejection reason")
    text = "rejected"
    set_data("result", "rejected")
    set_data("rejection_reason", rejection_reason)
else:
    set_data("result", "approved")
    text = "approved"

display_markdown(f"""
# Request {text}

Review completed by {user.email}
                 """, end_program=True, button_text=None)