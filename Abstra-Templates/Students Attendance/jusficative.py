from abstra.forms import *
import abstra.workflows as aw

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

def render(partial):
    if partial.get("ans") != None and partial.get("ans") == "Yes":
        return  (
            Page()
                .read("Please insert the justificative", key="justificative")
        )


stage = aw.get_stage()
class_skipped = stage["class_skipped"]
student = (  
    Page()
    .read_multiple_choice(f"You missed {class_skipped} classes,do tou have a justificative? ", ["Yes", "No"], key="ans")
    .reactive(render)
    .run()
)
ans = student["ans"]
if ans == "Yes":
    justificative = student["justificative"]
    aw.next_stage(
        [
            {
                "data": {
                    "justificative" : justificative,
                    "id": stage["id"],
                    "class_skipped": class_skipped,
                },
                "stage": "justificative-verification",
            }
        ]
    )