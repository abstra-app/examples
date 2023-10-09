import os
from abstra.forms import *
import stripe
import requests
import pandas as pd

# This form uses an environment variable. To make it work properly, add a Stripe API Key to your workspace's environment variables in the sidebar.
stripe.api_key = os.getenv('STRIPE_TEST_KEY')


def get_or_create_customer(email):
    res = stripe.Customer.list(email=email)
    customers = [cust for cust in res['data']]
    if len(customers):  # checks if the client already exists
        return customers[0]
    return stripe.Customer.create(email=email)


def checkout_session(price_data, customer, metadata):
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': price_data, 'quantity': 1}],
        payment_intent_data={'setup_future_usage': 'on_session'},
        mode='payment',
        customer=customer,
        success_url=f'https://console.abstracloud.com/',
        cancel_url=f'https://www.abstracloud.com/',
    )
    return session.url


email = read_email('Write your email')

# When applying this template use this authentication snippet for one step email validation

# auth_info = get_user()
# email = auth_info.email

# Create a customer
customer = get_or_create_customer(email)

days_to_expire = 360

total_usd = Page()\
    .display_markdown('''
## Our pricing
Pay as you go, buy credits for your execution
''')\
    .display_pandas(pd.DataFrame({
        'Resource': ['Forms', 'Hooks', 'Jobs'],
        'Price (USD)': ['$ 0.1 / Run', '$ 1 / Execution hour', '$ 1 / Execution hour']
    }).set_index('Resource'))\
    .read_currency(f'How many credits do you want?', currency='USD', initial_value=50, min=10, key='total_usd')\
    .run('Next')['total_usd']

currency = 'usd'

data = {
    'price_data': {
        'currency': currency,
        'product_data': {'name': 'Standard'},
        'unit_amount': total_usd * 100,
    },
    'metadata': {'resource': 'executions', 'total_usd': total_usd, 'days_to_expire': days_to_expire},
}


url = checkout_session(data['price_data'], customer['id'], data['metadata'])
execute_js('location.href=$context.url', context={
           'url': url})  # open stripe checkout
