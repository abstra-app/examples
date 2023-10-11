from abstra.forms import *
import pandas as pd


def get_cell(info):
    return df.loc[df["Email"] == email, info].item()


df = pd.read_excel("src/files/mock_data.xlsx")

# Here you can add your user authentication:
# user = get_user()
# email = user.email

# We'll use a simple email input for example purposes:
email = read_email("What's your email?", initial_value="anna@example.com")

result = df.loc[df["Email"] == email]


if email in result.values:
    name = get_cell("Name")
    points = get_cell("Points")
    redeem_date = get_cell("Redeem date")

    new_df = result.transpose(display_index=True)
    outfile = "/tmp/output.xlsx"
    output = new_df.to_excel(outfile)

    Page().display_markdown(
        f"""
## Hey {name}!
So far you've accumulated **{points}** points.
They can be reedemed from =={redeem_date}== onwards."""
    ).display("Here is your info in spreadsheet format.").display_pandas(
        new_df
    ).display_file(
        outfile, download_text="Download it here"
    ).run()

    Page().display("See you next time!").display_image(
        "https://media1.giphy.com/media/QsllPdKLHJMh6oLWSC/giphy.gif?cid=ecf05e47cllrr4vhdnrejbflfianu0ndxv9vvhlcikagt35d&rid=giphy.gif&ct=g"
    ).run()
else:
    display("Sorry, can't find this user!")
