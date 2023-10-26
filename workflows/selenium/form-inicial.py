from abstra.forms import *
from abstra.workflows import get_stage, next_stage

stage = get_stage()

# Get user information

name = read("Insert your name?")
email = read("Insert your email?")

stage["name"] = name
stage["email"] = email

# Get user choice

selected_option = read_multiple_choice(
    "Witch information would you like to visualize?",
    ["Main headlines of the day", "Stock exchange indexes"],
)

stage["selected_option"] = selected_option

# Define next stage based on user choice

if selected_option == "Main headlines of the day":
    new_stage = next_stage([{"stage": "News"}])
elif selected_option == "Stock exchange indexes":
    new_stage = next_stage([{"stage": "Stocks"}])
