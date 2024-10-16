import requests
import json

client = requests.Session()

headers = {
    "api-key": "RXNzS3Z3VmRnVkJKc25ZQnJHSkE",
    "Content-Type": "application/json"
}

base_url = "https://sms.arkesel.com/api/v2/sms/send"

recipients = ["233555560810"]

# SEND SMS
sms_payload = {
    "sender": "RAININ MALL",
    "message": "You have been selected as one of our loyal customers. Click here to receive your reward https://smconf.gikace.dev/login",
    "recipients": recipients
}

try:
    response = client.post(url=base_url, headers=headers, json=sms_payload)
    response.raise_for_status()
    print(response.text)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

#"You have been selected as one of our loyal customers. Click here to receive your reward https://smconf.gikace.dev/login",