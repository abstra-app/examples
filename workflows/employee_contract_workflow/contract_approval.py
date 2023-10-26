from abstra.forms import *
import abstra.workflows as aw
import pathlib
import os

# Here we get some info from the stage of the workflow that is running
stage = aw.get_stage()
output_filepath = stage["output_filepath"]
document_filename = stage["document_filename"]
team_id = stage["id"]
taxpayer_id = stage["taxpayer_id"]


# Now we create a function to render a new form if the user rejects the document
def render(partial):
    if len(partial) != 0:
        if partial.get("is_personal_data_problem") == [False]:
            return (
                Page()
                .read_file(
                    "Upload your changed contract", required=False, key="contract"
                )
                .read_textarea(
                    "Comments",
                    required=False,
                    placeholder="Put here your comments about the problems",
                    key="comments",
                )
            )


# Down here we discuss the approval or rejection of the document:
contract_approval = (
    Page()
    .display(f"Document Approval - {document_filename}", size="large")
    .display(
        f'Please read the "{document_filename}" document and indicate your approval or rejection below. '
    )
    .display_file(output_filepath, download_text="Click here to download the document")
    .run(actions=["Approve", "Reject"])
)

if contract_approval.action == "Reject":
    contract_reject = (
        Page()
        .read_checklist(
            "Does the contract have any personal data error?",
            [{"label": "Yes", "value": True}, {"label": "No", "value": False}],
            key="is_personal_data_problem",
            multiple=False,
        )
        .reactive(render)
        .run("Send")
    )

    contract_reject_list = [c for c in contract_reject.values()]

    if contract_reject["is_personal_data_problem"][0]:
        new_stage = aw.next_stage(
            [
                {
                    "assignee": stage["email"],
                    "data": {"id": team_id},
                    "stage": "update-team",
                }
            ]
        )
    if contract_reject["is_personal_data_problem"][0] == False:
        if contract_reject["contract"]:
            contract_filepath = contract_reject["contract"].file.name
            new_output_filepath = contract_filepath
        else:
            new_output_filepath = output_filepath
        comments = contract_reject["comments"]

    new_stage_contract = aw.next_stage(
        [
            {
                "assignee": "foo@company.co",
                "data": {
                    "id": team_id,
                    "comments": comments,
                    "new_output_filepath": new_output_filepath,
                    "output_filepath": output_filepath,
                    "document_filename": document_filename,
                    "taxpayer_id": taxpayer_id,
                },
                "stage": "contract-review",
            }
        ]
    )

else:
    new_stage = aw.next_stage(
        [
            {
                "assignee": stage["email"],
                "data": {
                    "id": team_id,
                    "document_filename": document_filename,
                    "output_filepath": output_filepath,
                    taxpayer_id: "taxpayer_id",
                },
                "stage": "qd3a67kfle",  # contract-signature
            }
        ]
    )

    PERSISTANT_FOLDER = pathlib.Path(os.environ.get("ABSTRA_FILES_FOLDER", "/tmp"))
    contract_folder = PERSISTANT_FOLDER / "contracts"
    contract_folder.mkdir(parents=True, exist_ok=True)
