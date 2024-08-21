"""
This Tax Calculator was made with our Brazillian friends in mind :)
Feel free to include, exclude or modify in any way the taxes you wish to calculate and currency (in our case, R$/brl).
"""

from abstra.forms import *


def tax_calculator(value, cofins, csll, irpj, pis):
    tax_total = 100 - (cofins + csll + irpj + pis)
    if irpj * (value / tax_total) < 10:
        tax = 100 - (cofins + csll + pis)
        irpj_brl = 0
    else:
        tax = tax_total
        irpj_brl = round(irpj * (value / tax), 2)
    cofins_brl = round(cofins * (value / tax), 2)
    csll_brl = round(csll * (value / tax), 2)
    pis_brl = round(pis * (value / tax), 2)
    invoice_value = round(value / (tax / 100), 2)
    if (cofins_brl + csll_brl + pis_brl) < 10:
        cofins_brl = 0
        csll_brl = 0
        pis_brl = 0
        invoice_value = value
    return cofins_brl, csll_brl, irpj_brl, pis_brl, invoice_value


invoice_data = (
    Page()
    .display("Hello! Fill in the data below:")
    .read_currency("Invoice value without taxes", currency='BRL', key="amount")
    .read_number("Cofins (%)", key="cofins")
    .read_number("Csll (%)", key="csll")
    .read_number("Irpj (%)", key="irpj")
    .read_number("Pis (%)", key="pis")
    .run("Send")
)

amount = invoice_data["amount"]
cofins  = invoice_data["cofins"]
csll  = invoice_data["csll"] 
irpj  = invoice_data["irpj"]
pis = invoice_data["pis"]

cofins_brl, csll_brl, irpj_brl, pis_brl, invoice_value_brl = tax_calculator(
    amount, cofins, csll, irpj, pis
)

Page()\
    .display(f"Invoice value with taxes: R$ {invoice_value_brl:.02f}")\
    .display(f"Cofins: R$ {cofins_brl:.02f}")\
    .display(f"Csll: R$ {csll_brl:.02f}")\
    .display(f"Irpj: R$ {irpj_brl:.02f}")\
    .display(f"Pis: R$ {pis_brl:.02f}")\
    .run("Ok, got it!")
