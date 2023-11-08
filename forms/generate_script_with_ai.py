import openai
from abstra.forms import *
import json
import os
import pandas as pd
import requests


openai.api_key = os.environ.get("OPENAI_API_KEY")


def comment(text):
    return f'\n\n\n"""\n{text}\n"""\n'


# script any language
query_example = "Reads coefficients of a quadratic formula and display its roots"
query = read_textarea("What you want your script to do?", initial_value=query_example)
prompt += comment("\n".join(["example:", query, "Simplest solution"]))

completion = (
    "from abstra.forms import *\n\n"
    + openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=500,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    .choices[0]
    .text.split('"""\nexample:')[0]
)

page = (
    Page()
    .read_code(
        "Here is your initial code, edit away!",
        initial_value=completion,
        language="python",
        key="code",
    )
    .run("Copy this code")
)

execute_js(
    "navigator.clipboard.writeText($context.code)", context={"code": page["code"]}
)

display_link("https://cloud.abstra.io", link_text="Go to your workspace")
