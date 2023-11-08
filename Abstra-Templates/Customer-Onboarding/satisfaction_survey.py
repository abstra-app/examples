from abstra.forms import *
import abstra.workflows as aw
from abstra.tables import insert

"""
Simple satisfaction survey
"""
satisfaction_survey = (
    Page()
    .display("Satisfaction Survey", size="large")
    .display(
        "We want to know how you feel about our services. Please answer the following questions."
    )
    .read_dropdown(
        "How would you rate our products?",
        [
            {"label": "Very good", "value": "very_good"},
            {"label": "Good", "value": "good"},
            {"label": "Regular", "value": "regular"},
            {"label": "Bad", "value": "bad"},
            {"label": "Very bad", "value": "very_bad"},
        ],
    )
    .read_dropdown(
        "How would you rate our prices?",
        [
            {"label": "Very good", "value": "very_good"},
            {"label": "Good", "value": "good"},
            {"label": "Regular", "value": "regular"},
            {"label": "Bad", "value": "bad"},
            {"label": "Very bad", "value": "very_bad"},
        ],
    )
    .read_dropdown(
        "How would you rate our website?",
        [
            {"label": "Very good", "value": "very_good"},
            {"label": "Good", "value": "good"},
            {"label": "Regular", "value": "regular"},
            {"label": "Bad", "value": "bad"},
            {"label": "Very bad", "value": "very_bad"},
        ],
    )
    .read_dropdown(
        "How would you rate our customer service?",
        [
            {"label": "Very good", "value": "very_good"},
            {"label": "Good", "value": "good"},
            {"label": "Regular", "value": "regular"},
            {"label": "Bad", "value": "bad"},
            {"label": "Very bad", "value": "very_bad"},
        ],
    )
    .read_dropdown(
        "How would you rate our customer support?",
        [
            {"label": "Very good", "value": "very_good"},
            {"label": "Good", "value": "good"},
            {"label": "Regular", "value": "regular"},
            {"label": "Bad", "value": "bad"},
            {"label": "Very bad", "value": "very_bad"},
        ],
    )
    .run("Send")
)

insert(
    "survey_database",
    {
        "product": satisfaction_survey["How would you rate our products?"],
        "prices": satisfaction_survey["How would you rate our prices?"],
        "website": satisfaction_survey["How would you rate our website?"],
        "customer_service": satisfaction_survey[
            "How would you rate our customer service?"
        ],
        "customer_support": satisfaction_survey[
            "How would you rate our customer support?"
        ],
    },
)
