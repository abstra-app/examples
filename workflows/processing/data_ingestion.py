import uuid, shutil
import abstra.forms as af
import abstra.common as ac
import abstra.workflows as aw
import utils

utils.check_user()

ingestion_id = str(uuid.uuid4())
aw.set_data("ingestion_id", ingestion_id)

upload = af.read_file("Upload new file")
shutil.copy(upload.file.name, ac.get_persistent_dir() / f"{ingestion_id}.csv")

af.Page().display("✅ File uploaded successfully").display(
    f"Your ingestion ID is {ingestion_id}"
).display(
    "When the processing is done, you will receive an email with the results."
).run()
