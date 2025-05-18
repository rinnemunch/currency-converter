import requests

API_KEY = '1b62f1c0422bd73fef545af0'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

def convert_currency(base, target, amount):
  url = BASE_URL + base
  response = requests.get(url)
  data = response.json()

  if response.status_code != 200 or data['result'] != 'success':
    print("Error: Could not fetch exchange rates: ")
    return

  rate = data['conversion_rates'].get(target)
  if not rate:
    print(f"Error: Invalid target currency '{target}'")
    return

  converted = amount * rate
  print(f"{amount} {base} = {converted:.2f} {target}")


convert_currency("USD", "EUR", 100)
