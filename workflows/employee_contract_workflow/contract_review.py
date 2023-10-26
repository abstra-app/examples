from abstra.forms import *
import abstra.workflows as aw
import shutil

stage = aw.get_stage()
output_filepath = stage["output_filepath"]
output_filepath_review = stage["new_output_filepath"]
document_filename = stage["document_filename"]
comments = stage["comments"]
team_id = stage["id"]
name = stage["name"]
email = stage["email"]
taxpayer_id = stage["taxpayer_id"]
reject_reason = stage["reject_reason"]


contract_review = (
    Page()
    .display(f"Document Review - {document_filename}", size="large")
    .display(
        f'Please thoroughly review the comments made on the document "{document_filename}" and make the necessary modifications.'
    )
    .display(f"Comments \n \n {comments}", key="comments")
    .display_file(
        output_filepath_review, download_text="Click here to download the document"
    )
    .run()
)

contract = read_file("Upload your changed contract")

# Copies file to destination directory
shutil.copy(contract.file.name, output_filepath)

aw.next_stage(
    [
        {
            "assignee": email,
            "data": {
                "id": team_id,
                "name": name,
                "email": email,
                "output_filepath": output_filepath,
                "document_filename": document_filename,
                "taxpayer_id": taxpayer_id,
            },
            "stage": "contract-approval",
        }
    ]
)
