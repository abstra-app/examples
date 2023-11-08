import abstra.forms as af
import abstra.workflows as aw
from abstra.tables import insert

"""
Here we are going to ask the client the churn reasons
"""
# Here we will create a form to know the churn reasons
churn_reasons = (
    af.Page()
    .read_dropdown(
        "Why are you leaving us?",
        [
            {"label": "Price", "value": "price"},
            {"label": "Customer service", "value": "customer_service"},
            {"label": "Customer support", "value": "customer_support"},
            {"label": "Product", "value": "product"},
            {"label": "Website", "value": "website"},
            {"label": "Other", "value": "other"},
        ],
        key="churn_reasons_dropdown",
    )
    .read_textarea(
        "Comments",
        required=False,
        placeholder="Put here your comments about the churn reasons",
        key="comments",
    )
    .run("Finish")
)
# Here we will insert the churn reasons in the churn_reasons table
insert(
    "churn_reasons",
    {
        "churn_reason": churn_reasons["churn_reasons_dropdown"],
        "comments": churn_reasons["comments"],
    },
)
