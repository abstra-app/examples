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
    .read("Invoice value without taxes (BRL)")
    .read("Cofins (%)")
    .read("Csll (%)")
    .read("Irpj (%)")
    .read("Pis (%)")
    .run("Send")
)


amount_brl, cofins_brl, csll_brl, irpj_brl, pis_brl = [
    float(x) for x in invoice_data.values()
]

cofins, csll, irpj, pis, invoice_value = tax_calculator(
    amount_brl, cofins_brl, csll_brl, irpj_brl, pis_brl
)

Page().display("Invoice value with taxes: R$ {}".format(invoice_value)).display(
    "Cofins: R$ {}".format(cofins)
).display("Csll: R$ {}".format(csll)).display("Irpj: R$ {}".format(irpj)).display(
    "Pis: R$ {}".format(pis)
).run(
    "Ok, got it!"
)
