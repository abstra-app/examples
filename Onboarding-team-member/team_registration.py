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


countries = [c.name for c in list(pycountry.countries)]

member = (Page().display("Personal Data", size='large')
                .read("Full name", key="name")
                .read_email("Email", key="personal_email")
                .read_date("Birth date", key="birth_date")
                .read_phone("Phone Number", key="phone_number")
                .read("National ID number (RG)", key="id_number")
                .read("ID number issued by", key="id_emited_by")
                .read_cpf("Individual Taxpayer Registration (CPF)", key="id_taxpayer")
                .read_dropdown("Country", countries, key="country")
                .read("State", key="state")
                .read("City", key="city")
                .read("Address (without number)", key="address")
                .read("Address number", key="number_address")
                .read("Address Complement", required=False, key="complement_address")
                .read("District", key="district")
                .read("Zip code", mask='00000-000', placeholder='00000-000', key="zip_code")
                .read("Shirt size", placeholder='M', key="shirt_size")
                .read("Dietary restrictions", required=False, placeholder='N/A', key="dietary_restrictions"))

bank_info_member = (Page().display("Bank Account Data", size='large')
                    .display("Please enter your bank account data. If you're subscribed to a company, please enter the company's bank account data.")
                    .read("Bank name", placeholder='Inter', key="bank_name")
                    .read("Bank account number", placeholder='0000000-0', key="bank_account_number")
                    .read("Bank branch code", placeholder='0001', key="bank_branch_code"))

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

if member["legal_entity_number"] is not None:
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
    'INSERT INTO "team"(name, email, birth_date, phone_number,\
  identification_number, id_emited_by, taxpayer_id, country, state,\
  city, address, number_address, complement_address, district, zip_code, shirt_size,\
  dietary_restrictions) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,\
  $14, $15, $16, $17) RETURNING id',
    params=[name, personal_email, birth_date, phone_number, id_number,
            id_emited_by, id_taxpayer, country, state, city, address, number_address,
            complement_address, district, zip_code, shirt_size, dietary_restrictions]
)
# Insert bank account data
run_finance('INSERT INTO "team_bank_account" (name, number, branch_code, team_id) VALUES($1, $2, $3, $4)',
            params=[bank_name, bank_account_number,
                    bank_branch_code, result[0]["id"]]
            )

# Insert company data
if name_company is not None:
    run_finance('INSERT INTO "team_entity_informations"(entity_number, name, state, city, address,\
      number_address, complement_address, district, zip_code,\
      team_id ) VALUES ( $1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
                params=[legal_entity_number, name_company, state_company, city_company,
                        company_address, company_number_address, company_complement_address,
                        company_district, company_zip_code, result[0]["id"]])

# name, id, email = name, result[0]["id"], personal_email

name, id, email, id_taxpayer = name, 31, personal_email, id_taxpayer

aw.next_stage([{
    "assignee": "catarina@abstra.app",
    "data": {"id": id, "name": name,
             "email": email, "id_taxpayer": id_taxpayer},
    "stage": "abstra-team-registration"
}])


# print(stage.data)
# print(stage)
