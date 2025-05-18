import tkinter as tk
from tkinter import ttk
import requests

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
root.title("Currency Converter")

root.geometry("400x300")
root.resizable(False, False)

root.mainloop()
