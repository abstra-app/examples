from abstra.forms import *

ans = read_number("What is the answer to life, the universe, and everything?")
# For more input widgets, see: https://docs.abstracloud.com/reference/widgets

if ans == 42:
    display("Correct!")
else:
    display("Incorrect!")

display_link(
    "https://docs.abstracloud.com/reference/widgets",
    link_text="See docs for more input and output widgets",
)
