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


if __name__ == "__main__":
  print("Currency Converter")
  print("Example codes: USD, EUR, JPY, GBP, AUD")

  base = input("Enter base currency (e.g. USD): ").upper()
  target = input("Enter target currency (e.g. EUR): ").upper()

  if not base.isalpha() or not target.isalpha():
    print("Currency codes must only contain letters (e.g., USD, EUR)")
  else:
    try:
      amount = float(input("Enter amount to convert: "))
      convert_currency(base, target, amount)
    except ValueError:
      print("Please enter a valid number.")
