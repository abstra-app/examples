from abstra.forms import *
import pandas as pd


def extra_fields(data):
    """
    Get the extra fields according to the dilution type
    """

    if not data or not "dilution_type" in data:
        return Page()
    elif data.get("dilution_type") == "percent":
        return Page().read_number(
            "How much % was reserved", key="amount", required=False
        )
    elif data.get("dilution_type") == "cap":
        return (
            Page()
            .read_currency("How much was invested?", key="amount", required=False)
            .read_currency("How much was the cap?", key="cap", required=False)
        )
    elif data.get("dilution_type") == "mfn":
        return Page().read_currency(
            "How much was invested?", key="amount", required=False
        )
    elif data.get("remaining"):
        return Page()


def add_to_cap_table(entity_name, round_name, percent, date):
    """
    Add informations in cap table
    """
    cap_table_entries.append(
        {
            "Entity": entity["name"],
            "Round": dilution["name"],
            "%": f"{(100 * percent * remaining_space):.2f}%",
            "Signature Date": date,
        }
    )


# Insert data manually or with a spreadsheet
data_sent = read_multiple_choice(
    "How would you like to enter the investors' data?", ["Manually", "Via spreadsheet"]
)

if data_sent == "Manually":
    dilution_schema = ListItemSchema().read(
        "What is the name of this round?", key="name"
    )

    dilutions = read_list(dilution_schema, key="dilutions", max=10, min=1)

    for dilution in dilutions:
        dilution_types = [
            {"label": "Fixed %", "value": "percent"},
            {"label": "Fixed cap", "value": "cap"},
            {"label": "MFN", "value": "mfn"},  # mfn: most favored nation
            {"label": "Remaining %", "value": "remaining"},
        ]

        entity_schema = (
            ListItemSchema()
            .read("Name", key="name")
            .read_dropdown(
                "What kind of dilution is that?", dilution_types, key="dilution_type"
            )
            .read_date("When did it happen?", key="date")
            .reactive(extra_fields)
        )

        dilution["entities"] = (
            Page()
            .display(f"Members in '{dilution['name']}'")
            .read_list(entity_schema, key="entities")
            .run()
        )
else:
    Page().display(
        "Download the spreadsheet below and fill it with your investors' info:"
    ).display_file("src/files/investors_data_template.xlsx").run()

    rounds_file = read_file("Upload your spreadsheet with the investors' list:")

    rounds = rounds_file.file
    data = pd.ExcelFile(rounds)
    sheet_name = data.sheet_names[0]
    df = pd.read_excel(rounds, sheet_name, header=0, decimal=".")
    normalized_columns = [x.lower().replace(" ", "_") for x in df.columns]
    df.columns = normalized_columns

    rounds_name = df["round"].unique()
    dilutions = []
    for round_name in rounds_name:
        dilution = {}
        dilution["name"] = round_name
        entity_value = []
        df_round_name = df[df["round"] == round_name].drop("round", axis=1)
        dilution["entities"] = {"entities": df_round_name.to_dict(orient="records")}
        dilutions.append(dilution)

# Cap table calculation

cap_table_entries = []
remaining_space = 1
dilutions.reverse()

last_min_cap = None
for dilution in dilutions:
    dilution_in_round = 0

    percent_entities = filter(
        lambda entity: entity["dilution_type"] == "percent",
        dilution["entities"]["entities"],
    )

    for entity in percent_entities:
        percent = entity["amount"] / 100

        dilution_in_round = dilution_in_round + percent
        add_to_cap_table(entity["name"], dilution["name"], percent, entity["date"])

    cap_entities = filter(
        lambda entity: entity["dilution_type"] == "cap",
        dilution["entities"]["entities"],
    )
    min_cap = None
    for entity in cap_entities:
        percent = entity["amount"] / entity["cap"]

        dilution_in_round = dilution_in_round + percent
        add_to_cap_table(entity["name"], dilution["name"], percent, entity["date"])

        if min_cap == None or entity["cap"] < min_cap:
            min_cap = entity["cap"]

    mfn_entities = filter(
        lambda entity: entity["dilution_type"] == "mfn",
        dilution["entities"]["entities"],
    )
    if last_min_cap:
        for entity in mfn_entities:
            percent = entity["amount"] / last_min_cap
            dilution_in_round = dilution_in_round + percent
            add_to_cap_table(entity["name"], dilution["name"], percent, entity["date"])
    elif last_min_cap == None and len(list(mfn_entities)) != 0:
        display(
            "Once you have no fixed cap investors in next round, MFNs will be ignored for now"
        )

    remaining_entities = list(
        filter(
            lambda entity: entity["dilution_type"] == "remaining",
            dilution["entities"]["entities"],
        )
    )
    if len(remaining_entities) > 0:
        for entity in remaining_entities:
            percent = (1 - dilution_in_round) / len(remaining_entities)

            add_to_cap_table(entity["name"], dilution["name"], percent, entity["date"])

        dilution_in_round = 1

    remaining_space = 1 - dilution_in_round
    last_min_cap = min_cap

if len(cap_table_entries) == 0:
    display("No data was entered")

else:
    df = pd.DataFrame.from_records(cap_table_entries)
    df = df.sort_values(by="Signature Date")
    df["Signature Date"] = pd.to_datetime(df["Signature Date"]).dt.strftime("%Y-%m-%d")
    df = df.set_index("Entity")
    df.to_csv("/tmp/cap_table.csv", index=False)

    Page().display_pandas(df, full_width=True).display_file(
        "/tmp/cap_table.csv", download_text="Download your cap table here"
    ).run()
