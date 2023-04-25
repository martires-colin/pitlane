# By Colin Martires

from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# cmartires1440@gmail.com twilio account details
# account_sid = "AC28c7833370d8c29f70a9c65185280e0c"
# auth_token = env.get('TWILIO_AUTH_TOKEN')
# twilio_number = '+18552607353'

# cmartires@nevada.unr.edu twilio account details
account_sid = "ACe89bcf18f6bb76ead265dd32725c48fe"
auth_token = env.get('TWILIO_AUTH_TOKEN')
twilio_number = '+18888143417'
