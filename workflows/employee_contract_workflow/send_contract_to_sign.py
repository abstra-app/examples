import abstra.workflows as aw
import requests
import os
from datetime import datetime, timedelta
import base64
import dotenv

dotenv.load_dotenv()


def create_signer(signer_data, cs_token, cs_subdomain):
    create_signer_response = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/signers?access_token={cs_token}",
        headers=headers,
        json=signer_data,
    )

    signer_key = create_signer_response.json()["signer"]["key"]
    return signer_key


def add_signer_to_document(
    document_key, signer_key, cs_token, cs_subdomain, sign_as="sign"
):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    body = {
        "list": {
            "document_key": document_key,
            "signer_key": signer_key,
            "sign_as": sign_as,
            "refusable": False,
            "message": ""
            # "message": f"Prezado/a {signer_name}, \n siga para a assinatura da Abstra . \n\n Em caso de dúvidas, entrar em contato com admin@abstra.app."
        }
    }

    add_signer_response = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/lists?access_token={cs_token}",
        headers=headers,
        json=body,
    )

    # Send notification to signer
    notification_body = {
        "request_signature_key": add_signer_response.json()["list"][
            "request_signature_key"
        ],
        "message": "Prezado/a, siga para a Assinatura do Contrato. \n\n Em caso de dúvidas, entrar em contato com admin@abstra.app.",
    }

    add_signer_notification = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/notifications?access_token={cs_token}",
        headers=headers,
        json=notification_body,
    )

    return add_signer_response.json()


# Set initial variables
stage = aw.get_stage()

filepath = stage["output_filepath"]
name = stage["name"]
id_taxpayer = stage["id_taxpayer"]
email = stage["email"]

cs_token = os.getenv("CLICKSIGN_TOKEN")
# cs_subdomain = 'sandbox' if os.getenv(
#    "ABSTRA_ENVIRONMENT") != "production" else 'app'
cs_subdomain = "app"

# signers = requests.get(
#    f'https://{cs_subdomain}.clicksign.com/api/v1/signers?access_token={cs_token}')

deadline = (datetime.now() + timedelta(days=89)).strftime("%Y-%m-%dT%H:%M:%S-03:00")

headers = {"Content-Type": "application/json", "Accept": "application/json"}


with open(filepath, "rb") as docx_file:
    base64_encoded = base64.b64encode(docx_file.read()).decode("utf-8")

# Create document object
document_data = {
    "document": {
        "path": f"/Contratos de Onboarding Abstra/{filepath.split('/')[-1]}",
        "content_base64": f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_encoded}",
        "deadline_at": deadline,
        "auto_close": True,
        "locale": "pt-BR",
        "sequence_enabled": False,
        "remind_interval": 7,
        "block_after_refusal": False,
    }
}

# Upload document to Clicksign
upload_document_response = requests.post(
    f"https://{cs_subdomain}.clicksign.com/api/v1/documents?access_token={cs_token}",
    headers=headers,
    json=document_data,
)


document_key = upload_document_response.json()["document"]["key"]


# Create signer object
signer_data = {
    "signer": {
        "email": email,
        "auths": ["email"],
        "name": name,
        "documentation": id_taxpayer,
        "birthday": "",
        "communicate_by": "email",
        "delivery": "email",
        "phone_number": "",
        "selfie_enabled": False,
        "handwritten_enabled": False,
        "official_document_enabled": False,
        "liveness_enabled": False,
        "facial_biometrics_enabled": False,
    }
}


signer_data = {
    "key": create_signer(signer_data, cs_token, cs_subdomain),
    "sign_as": "contractee",
}

abstra_signer_data = {"key": os.getenv("ADM_CLICKSIGN_KEY"), "sign_as": "administrator"}

signers = [signer_data, abstra_signer_data]


# Add signer to document
for signer in signers:
    add_signer_to_document(
        document_key, signer["key"], cs_token, cs_subdomain, signer["sign_as"]
    )
