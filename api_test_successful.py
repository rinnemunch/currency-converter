# This file was used to confirm successful API response
# You can delete or archive it later

import requests

API_KEY = '1b62f1c0422bd73fef545af0'

url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

response = requests.get(url)
data = response.json()

print(data)
