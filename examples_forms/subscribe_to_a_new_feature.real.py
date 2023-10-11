from abstra.forms import *

display("Hi there. Thanks for your interest in our upcoming features!")

display("We're almost ready to launch. Let's sign you up to get the news first-hand.")

fname = read("Firstly, what is your first name?")

lname = read("What is your last name?")

email = read_email("Great! What's your email?")

display(f"All set, {fname}! You'll be notified as soon as we launch 😎🚀")
