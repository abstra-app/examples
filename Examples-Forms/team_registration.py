from abstra.forms import *
from abstra.tables import run
from datetime import datetime

# Here you can add your company's authentication.
# user = get_user()
# if not user.email.endswith('@mycompany.com'):
# exit()


def add_member(
    name,
    email,
    start_date,
    position,
    birth_date,
    phone_number,
    id_number,
    id_emited_by,
    id_taxpayer,
    company_email,
    country,
    state,
    city,
    address,
    number_address,
    complement_address,
    district,
    zip_code,
    bank_name,
    bank_account_number,
    bank_branch_code,
    legal_entity_number,
    name_company,
    state_company,
    city_company,
    company_address,
    company_number_address,
    company_complement_address,
    company_district,
    company_zip_code,
    shirt_size,
):
    sql = """
        INSERT INTO members (name, email, start_date, position, birth_date, phone_number, id_number,\
     id_emited_by, id_taxpayer, company_email, country, state, city, address, number_address, complement_address,\
     district, zip_code, bank_name, bank_account_number, bank_branch_code, legal_entity_number, name_company,\
     state_company, city_company, company_address, company_number_address, company_complement_address, company_district,\
     company_zip_code, shirt_size)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10,\
                $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,\
                $21, $22, $23, $24, $25, $26, $27, $28, $29, $30,\
                $31)
        RETURNING id;
    """
    params = [
        name,
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    ]
    return run(sql, params)


def update_member(
    email,
    start_date,
    position,
    birth_date,
    phone_number,
    id_number,
    id_emited_by,
    id_taxpayer,
    company_email,
    country,
    state,
    city,
    address,
    number_address,
    complement_address,
    district,
    zip_code,
    bank_name,
    bank_account_number,
    bank_branch_code,
    legal_entity_number,
    name_company,
    state_company,
    city_company,
    company_address,
    company_number_address,
    company_complement_address,
    company_district,
    company_zip_code,
    shirt_size,
):
    sql = """
        UPDATE members
        SET email = $1, start_date = $2, position = $3, birth_date = $4, phone_number = $5, id_number = $6,\
        id_emited_by = $7, id_taxpayer = $8, company_email = $9, country = $10, state = $11, city = $12, address = $13,\
        number_address = $14, complement_address = $15, district = $16, zip_code = $17, bank_name = $18,\
        bank_account_number = $19, bank_branch_code = $20, legal_entity_number = $21, name_company = $22,\
        state_company = $23, city_company = $24, company_address = $25, company_number_address = $26,\
        company_complement_address = $27, company_district = $28, company_zip_code = $29, shirt_size = $30
        WHERE id = $31;
    """
    params = [
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    ]
    return run(sql, params)


def list_member():
    sql = """
        SELECT id, name, email FROM members;
    """
    return run(sql)


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


registration = read_multiple_choice(
    "Hello! What would you like to do?",
    [
        {"label": "Register a new member of team", "value": "new_member"},
        {"label": "Update a member information", "value": "update_member"},
    ],
)


def get_member_data(member_id):
    sql = """
        SELECT name, email, start_date, position, birth_date, phone_number, id_number,\
     id_emited_by, id_taxpayer, company_email, country, state, city, address, number_address,\
     complement_address, district, zip_code, bank_name, bank_account_number, bank_branch_code, legal_entity_number,\
     name_company, state_company, city_company, company_address, company_number_address,\
     company_complement_address, company_district, company_zip_code, shirt_size
        FROM members
        WHERE id = $2;
    """
    params = [member_id]
    display(
        "Congrats on the new team member! Their info has added to your database.",
        button_text="See you next time",
    )
    return run(sql, params)[0]


if registration == "new_member":
    member = (
        Page()
        .display(
            "Ok, to register a new member please fill in the following information:"
        )
        .read("Full name")
        .read_email("Personal Email")
        .read_date("Start date at company")
        .read("Position")
        .read_date("Birth date")
        .read_phone("Phone Number")
        .read("National ID number")
        .read("ID number emited by")
        .read("Social Security/ Individual Taxpayer Registration")
        .read_email("Company email")
        .read("Country")
        .read("State")
        .read("City")
        .read("Address")
        .read("Address number")
        .read("Address Complement", required=False)
        .read("District")
        .read("Zip code")
        .read("Bank Name")
        .read("Bank account number")
        .read("Bank branch code")
        .read("Legal entities number", required=False)
        .read("Company name", required=False)
        .read("Company state", required=False)
        .read("Company city", required=False)
        .read("Company address", required=False)
        .read("Company address number", required=False)
        .read("Company address complement", required=False)
        .read("Company district", required=False)
        .read("Company zip code", required=False)
        .read("Shirt size")
        .run("Send")
    )

    (
        name,
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    ) = member.values()

    start_date = preprocessing_date(start_date)
    birth_date = preprocessing_date(birth_date)
    phone_number = phone_number.raw

    add_member(
        name,
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    )

    display(
        "Congrats on the new team member! Their info has added to your database.",
        button_text="See you next time",
    )

    # Here you'll need to set your database's query statement in order to properly update it
    # We'll continue this example without doing so to keep the data stable
    # team_statement = tables.statement(id="your_statement_id")
    # result = team_statement.run(params={"name": name, "email": personal_email, "start_date": start_date,\
    #                                     "position": position, "birth_date": birth_date, "phone_number": phone_number,\
    #                                     "id_number": id_number, "id_emited_by": id_emited_by,\
    #                                     "taxpayer_id": id_taxpayer, "company_email": company_email, "country": country,\
    #                                     "state": state, "city": city, "address": address, "number_address": number_address,\
    #                                     "complement_address": complement_address, "district": district, "zip_code": zip_code,\
    #                                     "shirt_size": shirt_size)

    # bank_statement = tables.statement(id="your_statement_id")
    # bank_statement.run(params={"bank_name": bank_name, "number": bank_account_number,\
    #                            "branch_code": bank_branch_code, "team_id": result[0]["id"]})

    # if name_company is not None:
    #     entity_statement = tables.statement(id="your_statement_id")
    #     entity_statement.run(params={"entity_number": legal_entity_number, "name_company": name_company,\
    #                                 "state_company": state_company, "city_company": city_company,\
    #                                 "company_address": company_address, "company_number_address": company_number_address,\
    #                                 "company_complement_address": company_complement_address, "company_district": company_district,\
    #                                 "company_zip_code": company_zip_code, "team_id": result[0]["id"]})


elif registration == "update_member":
    member_database = list_member()  # [{ id, name, email }]

    member = [
        {"label": f'{customer["name"]} ({customer["email"]})', "value": customer["id"]}
        for customer in member_database
    ]  # [{ label, value }]

    customer_id = read_dropdown("Which customer do you want to update data", member)
    member = (
        Page()
        .display("Perfect. Please update the information you need below:")
        .read_email("Personal Email", required=False)
        .read_date("Start date at company", required=False)
        .read("Position", required=False)
        .read_date("Birth date", required=False)
        .read_phone("Phone Number", required=False)
        .read("National ID number", required=False)
        .read("ID number emited by", required=False)
        .read("Social Security/ Individual Taxpayer Registration", required=False)
        .read_email("Company email", required=False)
        .read("Country", required=False)
        .read("State", required=False)
        .read("City", required=False)
        .read("Address", required=False)
        .read("Address number", required=False)
        .read("Address Complement", required=False)
        .read("District", required=False)
        .read("Zip code", required=False)
        .read("Bank Name", required=False)
        .read("Bank account number", required=False)
        .read("Bank branch code", required=False)
        .read("Legal entities number", required=False)
        .read("Company name", required=False)
        .read("Company state", required=False)
        .read("Company city", required=False)
        .read("Company address", required=False)
        .read("Company address number", required=False)
        .read("Company address Complement", required=False)
        .read("Company district", required=False)
        .read("Company zip code", required=False)
        .read("Shirt size", required=False)
        .run("Send")
    )

    (
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    ) = member.values()

    start_date = preprocessing_date(start_date)
    birth_date = preprocessing_date(birth_date)
    if phone_number != None:
        phone_number = phone_number.raw

    update_member(
        email,
        start_date,
        position,
        birth_date,
        phone_number,
        id_number,
        id_emited_by,
        id_taxpayer,
        company_email,
        country,
        state,
        city,
        address,
        number_address,
        complement_address,
        district,
        zip_code,
        bank_name,
        bank_account_number,
        bank_branch_code,
        legal_entity_number,
        name_company,
        state_company,
        city_company,
        company_address,
        company_number_address,
        company_complement_address,
        company_district,
        company_zip_code,
        shirt_size,
    )

    # Here you'll need to set your database's query statement in order to properly update it
    # We'll continue this example without doing so to keep the data stable
    # statement = tables.statement(id="your_statement_id")
    # result = statement.run(params={"email": personal_email, "start_date": start_date, "position": position,\
    #                                "birth_date": birth_date, "phone_number": phone_number, "id_number": id_number,\
    #                                "id_emited_by": id_emited_by, "taxpayer_id": id_taxpayer, "company_email": company_email,\
    #                                "country": country, "state": state, "city": city, "address": address,\
    #                                "number_address": number_address, "complement_address": complement_address,\
    #                                "district": district, "zip_code": zip_code, "shirt_size": shirt_size,\
    #                              \
    #                                "exit_date":departure_date, "team_member_id": team_member_id})

    # bank_statement = tables.statement(id="your_statement_id")
    # bank_statement.run(params={"name": bank_name, "number": bank_account_number,\
    #                                 "branch_code": bank_branch_code, "team_member_id": team_member_id})

    # entity_statement = tables.statement(id="your_statement_id")
    # entity_statement.run(params={"entity_number": legal_entity_number, "name": name_company,\
    #                              "state": state_company, "city": city_company,\
    #                              "address": company_address, "number_address": company_number_address,\
    #                              "complement_address": company_complement_address, "district": company_district,\
    #                              "zip_code": company_zip_code, "team_member_id": team_member_id})

    display(
        "Great! The team member's info has been updated.",
        button_text="See you next time",
    )
