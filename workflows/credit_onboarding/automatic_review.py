from abstra.workflows import get_data, set_data
from time import sleep

name = get_data("name")
email = get_data("email")
income = get_data("income")
employer = get_data("employer")
loan_amount = get_data("loan_amount")
installments = get_data("installments")
score = get_data("score")

if loan_amount < 100000000:
    set_data("result", "approved")
else: 
    set_data("result", "rejected")
    set_data("rejection_reason", "Loan amount too high")

sleep(10)