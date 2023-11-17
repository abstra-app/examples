from abstra.forms import *
import abstra.workflows as aw
from abstra.tables import update,run


stage = aw.get_stage()
justificative = stage["justificative"]
class_skipped = stage["class_skipped"]
id = stage["id"]

def get_student_info(id):
    sql = """SELECT unjustified, justified FROM skippeds_classes WHERE id = $1;"""
    params = [id]
    return run(sql, params)[0]
all_student = get_student_info(id)
print(all_student)
justified = all_student["justified"]
unjustified = all_student["unjustified"]


supervisor = (
    Page()
    .read_multiple_choice(f"The student has a justificative:\n{justificative}\n, do you aprove it? ", ["Yes", "No"], key="ans")
    .run()
)
ans = supervisor["ans"]
if ans == "Yes":
    update("skippeds_classes",{"justified": justified + class_skipped,"unjustified": unjustified - class_skipped},{"id": id})
