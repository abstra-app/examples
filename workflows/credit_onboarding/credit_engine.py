from abstra.workflows import get_data, set_data
from time import sleep

name = get_data("name")
email = get_data("email")
income = get_data("income")
employer = get_data("employer")
loan_amount = get_data("loan_amount")
installments = get_data("installments")

if loan_amount > income * 0.3:
    set_data("score", "low")
    set_data("reason_low_score", "Value of the loan greater than 1/3 of the income")
else:
    set_data("score", "high")

sleep(10)