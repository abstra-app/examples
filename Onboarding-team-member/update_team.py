from abstra.forms import *
from run_finance import *
import abstra.workflows as aw
from datetime import datetime
import pycountry


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


stage = aw.get_stage()
team_id = stage["id"]
countries = [c.name for c in list(pycountry.countries)]

member = (Page().display("Personal Data", size='large')
                .read("Full name", required=False, key="name")
                .read_email("Email", required=False, key="personal_email")
                .read_date("Birth date", required=False, key="birth_date")
                .read_phone("Phone Number", required=False, key="phone_number")
                .read("National ID number (RG)", required=False, key="id_number")
                .read("ID number issued by", required=False, key="id_emited_by")
                .read_cpf("Individual Taxpayer Registration (CPF)", required=False, key="id_taxpayer")
                .read_dropdown("Country", countries, required=False, key="country")
                .read("State", required=False, key="state")
                .read("City", required=False, key="city")
                .read("Address (without number)", required=False, key="address")
                .read("Address number", required=False, key="number_address")
                .read("Address Complement", required=False, key="complement_address")
                .read("District", required=False, key="district")
                .read("Zip code", mask='00000-000', placeholder='00000-000', required=False, key="zip_code")
                .read("Shirt size", placeholder='M', required=False, key="shirt_size")
                .read("Dietary restrictions", required=False, placeholder='N/A', key="dietary_restrictions"))

bank_info_member = (Page().display("Bank Account Data", size='large')
                    .display("Please enter your bank account data. If you're subscribed to a company, please enter the company's bank account data.")
                    .read("Bank name", placeholder='Inter', required=False, key="bank_name")
                    .read("Bank account number", placeholder='0000000-0', required=False, key="bank_account_number")
                    .read("Bank branch code", placeholder='0001', required=False, key="bank_branch_code"))

company_member = (Page().display("Company Data", size='large')
                  .read_cnpj("Legal entities number (CNPJ)", required=False, key="legal_entity_number")
                  .read("Company name", required=False, key="name_company")
                  .read("Company state", required=False, key="state_company")
                  .read("Company city", required=False, key="city_company")
                  .read("Company address", required=False, key="company_address")
                  .read("Company address number (without number)", required=False, key="company_number_address")
                  .read("Company address complement", required=False, key="company_complement_address")
                  .read("Company district", required=False, key="company_district")
                  .read("Company zip code", required=False, mask='00000-000', placeholder='00000-000', key="company_zip_code"))


member = run_steps([member, bank_info_member, company_member])

name, personal_email, birth_date, phone_number, id_number,\
    id_emited_by, id_taxpayer, country, state, city, address, number_address,\
    complement_address, district, zip_code, shirt_size, dietary_restrictions = (member["name"],
                                                                                member["personal_email"], member["birth_date"], member[
                                                                                    "phone_number"], member["id_number"],
                                                                                member["id_emited_by"], member["id_taxpayer"], member[
                                                                                    "country"], member["state"], member["city"],
                                                                                member["address"], member["number_address"], member[
                                                                                    "complement_address"], member["district"],
                                                                                member["zip_code"], member["shirt_size"], member["dietary_restrictions"])

bank_name, bank_account_number, bank_branch_code = (
    member["bank_name"], member["bank_account_number"], member["bank_branch_code"])

legal_entity_number, name_company, state_company, city_company, company_address,\
    company_number_address, company_complement_address, company_district, company_zip_code = (member["legal_entity_number"],
                                                                                              member["name_company"], member[
                                                                                                  "state_company"], member["city_company"],
                                                                                              member["company_address"], member[
                                                                                                  "company_number_address"], member["company_complement_address"],
                                                                                              member["company_district"], member["company_zip_code"])


birth_date = preprocessing_date(birth_date)
phone_number = phone_number.raw
id_taxpayer = id_taxpayer.replace('.', '').replace('-', '')
legal_entity_number = legal_entity_number.replace(
    '.', '').replace('-', '').replace('/', '')

# Insert personal data
result = run_finance(
    'UPDATE "team" SET name = COALESCE($1, name), email = COALESCE($2, email), birth_date = COALESCE($3, birth_date),\
    phone_number = COALESCE($4, phone_number), identification_number = COALESCE($5, identification_number),\
    id_emited_by = COALESCE($6, id_emited_by), taxpayer_id = COALESCE($7, taxpayer_id), country = COALESCE($8, country),\
    state = COALESCE($9, state), city = COALESCE($10, city), address = COALESCE($11, address),\
    number_address = COALESCE($12, number_address), complement_address = COALESCE($13, complement_address),\
    district = COALESCE($14, district), zip_code = COALESCE($15, zip_code), shirt_size = COALESCE($16, shirt_size),\
    dietary_restrictions = COALESCE($17, dietary_restrictions) WHERE id = $18',
    params=[name, personal_email, birth_date, phone_number, id_number, id_emited_by,
            id_taxpayer, country, state, city, address, number_address, complement_address,
            district, zip_code, shirt_size, dietary_restrictions, team_id])


# Insert bank account data
run_finance('UPDATE "team_bank_account" SET name = COALESCE($1, name), number = COALESCE($2, number),\
    branch_code = COALESCE($3, branch_code) WHERE team_id = $4', params=[bank_name, bank_account_number,
                                                                         bank_branch_code, team_id]
            )


# Insert company data
run_finance('UPDATE "team_entity_informations" SET entity_number = COALESCE($1, entity_number), name = COALESCE($2, name),\
    state = COALESCE($3, state), city = COALESCE($4, city), address = COALESCE($5, address),\
    number_address = COALESCE($6, number_address), complement_address = COALESCE($7, complement_address),\
    district = COALESCE($8, district), zip_code = COALESCE($9, zip_code) WHERE team_id = $10',
            params=[legal_entity_number, name_company, state_company, city_company,
                    company_address, company_number_address, company_complement_address,
                    company_district, company_zip_code, team_id]
            )


name, id, email, id_taxpayer = name, team_id, personal_email, id_taxpayer
# name, id, email = name, 4, personal_email

aw.next_stage([{
    "assignee": personal_email,
    "data": {"id": team_id, "name": name,
             "email": email, "id_taxpayer": id_taxpayer},
}])
