from abstra.forms import *
from abstra.tables import *
import abstra.workflows as aw

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""
# def delete_data():
#     sql = """DELETE FROM skipped_classes;"""
#     params = []
#     return run(sql, params)     
# delete_data()
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


def get_student_info():
    sql = """SELECT name, unjustified FROM skippeds_classes;"""
    params = []
    return run(sql, params)
all_student = get_student_info()
print(all_student)
for student in all_student:
    if student["name"] == name:
        update("skippeds_classes",{"unjustified": student["unjustified"] + classes_skipped}, {"name": name})
inserting = insert("skippeds_classes", {"name": name, "unjustified": classes_skipped, "justified": 0}) 

# You can save and get information from the workflow context
aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                "id": inserting["id"],
                "class_skipped": classes_skipped,
            },
            "stage": 'jusficative',
        }
    ]
)