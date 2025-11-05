import requests
import json
from db.Migrations.CreateTableChat import up as ctc
from db.Migrations.CreateTableUsers import up as ctu

API_URL = "https://worldofansari.com/friends-api"
payload = {"query": ctc() + '\n' + ctu()}

try:
    response = requests.post(API_URL, json=payload, timeout=10)
    print(response.status_code)
    print(response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
