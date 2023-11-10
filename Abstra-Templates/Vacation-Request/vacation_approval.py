from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""
stage = get_stage()
manname = stage["manname"]
name = stage["name"]
email = stage["email"]
days = stage["days"]
start = stage["start"]
end = stage["end"]
reason = stage["reason"]
other = stage["other"]

# Now we are going to display the information about the employee to the team member analise its request

if reason == "other":
    reason = other
    
    display_html(f'''<head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Time-Off Request</h1>
        <h3>Subject: Time-Off Request Submission Confirmation from {name}</h3>
        <p>Dear Mr(s) [Manager Name],</p>
            
            <p>This message is to inform you that {name} has submitted a time-off request.
            <br>Below are the details of the requested leave for your review and approval:
            
        <br><br> Employee Name: {name}
            <br> Start Date: {start}
            <br> End Date: {end}
            <br> Duration: {days}
            <br> Reason: {other}
            
        <p> Should any additional information be required to process this request, please get in touch with the employee.<br> Your prompt attention to this matter would be much appreciated.</p>
            <p>  Kind Regards,
            <br>AbstraBot.</p>
                </body>
                <style>
                body {{
                    background-color: #F2F2F2;
                    font-family: Arial, sans-serif;
                    }}
                    h1 {{
                        color: #2C3E50;
                        text-align: center;
                        margin-bottom: 30px;
                        }}
        
                    h3 {{
                            color: #34495E;
                            text-align: left;
                            margin-bottom: 20px;
                        }}
                        
                    p {{
                            color: #2C3E50;
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 10px;
                            margin-left: 10px;
                            margin-right: 10px;
                        }}
                    </style>
                        ''')

def render(partial):
    if partial.get("approval") and partial.get("approval") == "no":
        return Page().read("Please specify:", key="specify")

def another(partial):
    if partial.get("approval") and partial.get("approval") == "yes":
        return Page().read("Required Documents:", key="documents")
    
approvation = (
    Page()
    .read_dropdown(
        "Do you aprove the request?",
        [
            {"label": "Yes", "value": "yes"},
            {"label": "No", "value": "no"},
        ],
        key="approval",
    )
    .reactive(render)
    .reactive(another)
    .run()              
)

if approvation.get("approval") == "no":
    next_stage(
    [
        {
            "data": {
                "approval": approvation.get("approval"),
                "specify": approvation.get("specify"),
                "name" : name ,
                "email" : email ,
            },
            "stage": "Reject Message",
        }
    ]
    )
else:
    next_stage(
    [
        {
            "data": {
                "approval": approvation.get("approval"),
                "documents": approvation.get("documents"),
                "name" : name , 
                "email" : email ,
            },
            "stage": "Required documents",
        }
    ]
    )