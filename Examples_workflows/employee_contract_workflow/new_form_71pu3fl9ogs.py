import abstra.forms as af
import abstra.workflows as aw

team_id = "0dd32514-3fbf-4ae4-97d4-055685368e3f"
email = "1@1.co"
name = "1"

aw.next_stage(
    [
        {
            "data": {
                "id": team_id,
                "email": email,
                "name": name,
            },
        }
    ]
)
