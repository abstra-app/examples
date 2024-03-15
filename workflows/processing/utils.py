import sys
import abstra.forms as af
import abstra.common as ac


def check_user():
    user = ac.get_user()
    if not user.email.endswith("@abstra.app"):
        af.display(
            "🚫 You must be an Abstra user to run this workflow", end_program=True
        )
        sys.exit(1)
