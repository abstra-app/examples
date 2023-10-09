from abstra.forms import *
from datetime import datetime
from abstra.tables import run

#Here you can add your company's authentication.
#user = get_user()
#if not user.email.endswith('@mycompany.com'):
  #exit()

def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date

def get_travel():

  travel = Page().display("Hello! To register a new travel, please add the information required in the fields below:")\
                .read("Travel purpose", key="purpose")\
                .read_date("Date of travel",key="date")\
                .read("Country of travel",key="country")\
                .read("City of travel",key="city")\
                .run("Send")
  return travel.values()

def insert_travel_db():
    purpose, travel_date, country, city = get_travel()
    travel_date = preprocessing_date(travel_date)
    
    sql = """
        INSERT INTO travel (purpose, date, country, city)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
    """
    params = [
        purpose,
        travel_date,
        country,
        city,
    ]
    return run(sql, params)

insert_travel_db()
display("All good! Your travel has been registered.")
