import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from tkinter import PhotoImage

API_KEY = '1b62f1c0422bd73fef545af0'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

def get_currency_list(base="USD"):
  url = BASE_URL + base
  response = requests.get(url)
  data = response.json()

  if response.status_code == 200 and data['result'] == 'success':
    return list(data['conversion_rates'].keys())
  else:
    return []

root = tk.Tk()
icon = PhotoImage(file="my_icon.png")
root.iconphoto(True, icon)
#for styles
style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 11))
style.configure("TCombobox", font=("Arial", 11))
root.title("Currency Converter")

currencies = get_currency_list()

base_label = ttk.Label(root, text="From: ")
base_label.pack(pady=(10,0), padx=10)

base_currency = ttk.Combobox(root, values=currencies, state="readonly")
base_currency.set("USD")
base_currency.pack(pady=(0,10), padx=10)

#dropdown
target_label = ttk.Label(root, text="To:")
target_label.pack(pady=(10,0), padx=10)

target_currency = ttk.Combobox(root, values=currencies, state="readonly")
target_currency.set("EUR")
target_currency.pack(pady=(0,10), padx=10)

#amount input
amount_label = ttk.Label(root, text="Amount:")
amount_label.pack(pady=(10,0), padx=10)

amount_entry = ttk.Entry(root)
amount_entry.pack(pady=(0,10), padx=10)


root.geometry("400x300")
root.resizable(False, False)

#==Result Label==
result_label = ttk.Label(root, text="")
result_label.pack(pady=(10,0), padx=10)

#convert function
def convert():
  base = base_currency.get()
  target = target_currency.get()
  try:
    amount = float(amount_entry.get())
  except ValueError:
    result_label.config(text="Enter a valid number.")
    return

  url = BASE_URL + base
  response = requests.get(url)
  data = response.json()

  if response.status_code != 200 or data['result'] != 'success':
    result_label.config(text="API error. Try again.")
    return

  rate = data['conversion_rates'].get(target)
  if not rate:
    result_label.config(text="Invalid target currency.")
    return

  converted = amount * rate
  result_label.config(text=f"{amount} {base} = {converted:.2f} {target}")
  timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
  with open("conversion_history.txt", "a") as file:
    file.write(f"{amount} {base} = {converted:.2f} {target} ({timestamp})\n")

#convert button
convert_btn = ttk.Button(root, text="Convert", command=convert)
convert_btn.pack(pady=(10,0), padx=10)

root.mainloop()
