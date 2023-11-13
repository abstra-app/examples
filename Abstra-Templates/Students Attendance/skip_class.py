from abstra.forms import *
from abstra.tables import *
import abstra.workflows as aw

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

# The professor will insert the information of the student that is skipping class
student = (
    Page()
    .read("What is the name of the student?", key="name")
    .read_number("How many classes has the student skipped?", key="classes_skipped")
    .run()
)
(
    name,
    classes_skipped,
) = student.values()

# You can save and get information from the workflow context
stage = aw.get_stage()
stage["name"] = name
stage["classes_skipped"] = classes_skipped

def get_student_info():
    sql = """SELECT name, unjustified FROM skipped_classes;"""
    params = []
    return run(sql, params)
all_student = get_student_info()
print(all_student)
for student in all_student:
    if student["name"] == name:
        update("skipped_classes",{"unjustified": student["unjustified"] + classes_skipped}, {"name": name})
        exit()
insert("skipped_classes", {"name": name, "justified": 0, "unjustified": classes_skipped}) 
