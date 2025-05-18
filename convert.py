import requests
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)

API_KEY = 'your_api_key_here'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

def get_currency_list(base="USD"):
  url = BASE_URL + base
  response = requests.get(url)
  data = response.json()

  if response.status_code == 200 and data['result'] == 'success':
    return list(data['conversion_rates'].keys())
  else:
    return []

def convert_currency(base, target, amount):
  url = BASE_URL + base
  response = requests.get(url)
  data = response.json()

  if response.status_code != 200 or data['result'] != 'success':
    print(Fore.RED + "Error: Could not fetch exchange rates: ")
    return

  rate = data['conversion_rates'].get(target)
  if not rate:
    print(Fore.RED + f"Error: Invalid target currency '{target}'")
    return

  converted = amount * rate
  print(Fore.GREEN + f"{amount} {base} = {converted:.2f} {target}")

  timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
  with open("conversion_history.txt", "a") as file:
    file.write(f"{amount} {base} = {converted:.2f} {target} ({timestamp})\n")


if __name__ == "__main__":
  print("Currency Converter")
  print("Fetching available currencies...\n")
  currencies = get_currency_list()
  print(", ".join(currencies))
  print()
  print("Example codes: USD, EUR, JPY, GBP, AUD")

  while True:
    base = input("Enter base currency (or 'q' to quit): ").upper()
    if base == "Q":
      break

    target = input("Enter target currency (or 'q' to quit): ").upper()
    if target == "Q":
      break

    if not base.isalpha() or not target.isalpha():
      print(Fore.YELLOW + "Currency codes must only contain letters (e.g., USD, EUR)")
    else:
      try:
        amount = float(input("Enter amount to convert: "))
        convert_currency(base, target, amount)
      except ValueError:
        print(Fore.YELLOW + "Please enter a valid number.")
