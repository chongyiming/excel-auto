import requests
import datetime
import base64
import json

url = "http://localhost:5678/webhook-test/startrader"





payload = {
    "message": {
        "text": "<u><b>answer</b></u>"
    }
}

# Send as JSON
response = requests.post(url, json=payload)
print(response.status_code, response.text)