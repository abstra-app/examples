from abstra.forms import *
from abstra.workflows import get_stage, next_stage

stage = get_stage()

# Get user information

name = read("Qual seu nome?")
email = read("Qual seu email?")

stage['name'] = name
stage['email'] = email

# Get user choice

selected_option = read_multiple_choice(
    "Qual informação você deseja visualizar?",[
        "Lista das principais manchetes do dia",
        "Índices das bolsa de valores"
    ]
)

stage['selected_option'] = selected_option

# Define next stage based on user choice

if selected_option == "Lista das principais manchetes do dia":
    new_stage = next_stage(
        [
            {
            "stage": "News"
            }
        ]
    )
elif selected_option == "Índices das bolsa de valores":
    new_stage = next_stage(
        [
            {
                "stage": "Stocks"
            }
        ]
    )