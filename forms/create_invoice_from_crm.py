import abstra.forms as hf
import json
import os
from datetime import date
from shutil import make_archive
from typing import Dict, List

# from simple_salesforce import Salesforce


class Invoice:
    def __init__(self, memo: str) -> None:
        self._m = memo + "\n"
        self._payments = []
        self._nPayments = 0

    def addPayment(self, amount: float, description: str) -> None:
        self._payments.append({"amount": amount, "description": description})
        self._nPayments = len(self._payments)

    def getInvoices(
        self,
    ) -> List[Dict[str, any]]:
        invoices = []
        for i in range(len(self._payments)):
            invoices.append(self._getInvoice(i))
        return invoices

    def _getInvoice(self, i: int) -> Dict[str, any]:
        payment = self._payments[i]
        if i == self._nPayments - 1:
            memo = self._m + "\n Final payment."
        else:
            remaining = sum([p["amount"] for p in self._payments[i + 1 :]])
            memo = self._m + "Payment: {} of {}\n".format(i + 1, self._nPayments)
            memo += "Remaining payment(s): ${}".format(remaining)
        return {
            "amount": payment["amount"],
            "description": payment["description"],
            "memo": memo,
        }


# sf =  Salesforce(
#         username=os.environ["SALESFORCE_USERNAME"],
#         password=os.environ["SALESFORCE_PASSWORD"],
#         security_token=os.environ["SALESFORCE_API_KEY"])

inputData = (
    hf.Page()
    .read("Please insert the product id", key="productId")
    .read_multiple_choice("Which color ?", ["Red", "Blue", "Brown"], key="colorType")
    .run("Send")
)
productId = inputData["productId"]
color = inputData["colorType"]

# opportunity = sf.Opportunity.get(productId)

opportunity = {
    "customer": "Ash",
    "description": "tenis novo",
    "productName": "Pokemon Snickers",
    "dateOfPurchase": date.today(),
    "price": 100,
}


data = {"customer": "John Doe", "price": 0, "productName": "Pokemon Snickers"}

payments = []

data["customer"] = opportunity["customer"]
data["description"] = opportunity["description"]
data["productName"] = opportunity["productName"]
data["dateOfPurchase"] = opportunity["dateOfPurchase"]
data["price"] = opportunity["price"]
data["type"] = color

invoice = Invoice("Product: " + data["productName"] + "-" + data["customer"])
invoice.addPayment(opportunity["price"], "Product price")

invoice.addPayment(round(0.2 * opportunity["price"], -1), "Taxes")

receiptTag = data["customer"] + "-" + str(data["dateOfPurchase"])

# Export invoices
filename = "/tmp/" + receiptTag + "/invoices.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
f = open(filename, "w")

# write json object to file
f.write(json.dumps(invoice.getInvoices()))

# close file
f.close()

zip_fname = make_archive(f"/tmp/{receiptTag}", "zip", f"/tmp/{receiptTag}")
f = open(zip_fname, "rb")
hf.display_file(f)
