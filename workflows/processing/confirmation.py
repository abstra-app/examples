import utils, shutil, sys
import pandas as pd
import abstra.forms as af
import abstra.common as ac
import abstra.workflows as aw

utils.check_user()

ingestion_id = aw.get_data("ingestion_id")
graph = ac.get_persistent_dir() / f"{ingestion_id}.png"
processed_file = ac.get_persistent_dir() / f"{ingestion_id}_processed.csv"

df = pd.read_csv(processed_file)

response = (
    af.Page()
    .display("Confirm the following data")
    .display_pandas(df)
    .display_image(graph, full_width=True)
    .display("Do you confirm the data?")
    .run(actions=["Yes", "No"])
)

if response.action == "No":
    af.display("Discarding the data.")
else:
    shutil.copy(graph, ac.get_persistent_dir() / "latest.png")
    af.display("Data confirmed. Updating to the latest version.", end_program=True)
    sys.exit(0)
