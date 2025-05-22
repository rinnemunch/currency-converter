import tkinter as tk
from tkinter import ttk, messagebox
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

BG_COLOR = "#0992db"

root = tk.Tk()
root.configure(bg=BG_COLOR)
icon = PhotoImage(file="my_icon.png")
root.iconphoto(True, icon)
root.title("PocketRates")
root.geometry("420x500")
root.resizable(False, False)

# --- Style ---
style = ttk.Style()
style.configure("Custom.TFrame", background=BG_COLOR)
style.configure("TLabel", font=("Segoe UI", 11), background=BG_COLOR)
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 11))

# Placeholder image
logo_img = PhotoImage(file="my_icon.png").subsample(13, 13) #image size

# Header Frame
header_color = "#001f4d"
header_frame = tk.Frame(root, bg=header_color, height=70)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)  # force height to stick


# App Name on Left
app_name = tk.Label(header_frame, text="PocketRates", fg="white", bg=header_color, font=("Segoe UI", 13, "bold"))
app_name.pack(side="left", padx=15)

center_frame = tk.Frame(header_frame, bg=header_color)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

logo_label = tk.Label(center_frame, image=logo_img, bg=header_color)
logo_label.image = logo_img
logo_label.pack(side="left", pady=5, padx=(0, 6))

# Right Side Placeholder
info_label = tk.Label(header_frame, text="v1.0", fg="white", bg=header_color, font=("Segoe UI", 10))
info_label.pack(side="right", padx=15)

# --- Main Frame ---
main_frame = ttk.Frame(root, padding=20, style="Custom.TFrame")
main_frame.pack(expand=True)

# --- Title ---
title = ttk.Label(main_frame, text="PocketRates", foreground="white", font=("Segoe UI", 16, "bold"))
title.pack(pady=(0, 20))

# --- Currency Data ---
currencies = get_currency_list()

# --- From Currency ---
ttk.Label(main_frame, text="From:", foreground="white").pack(pady=(5, 0))
base_currency = ttk.Combobox(main_frame, values=currencies, state="readonly", width=20)
base_currency.set("USD")
base_currency.pack(pady=5)

# --- To Currency ---
ttk.Label(main_frame, text="To:", foreground="white").pack(pady=(10, 0))
target_currency = ttk.Combobox(main_frame, values=currencies, state="readonly", width=20)
target_currency.set("EUR")
target_currency.pack(pady=5)

# --- Amount ---
ttk.Label(main_frame, text="Amount:", foreground="white").pack(pady=(10, 0))
amount_entry = ttk.Entry(main_frame, width=22)
amount_entry.pack(pady=5)

# --- Result Label ---
result_label = ttk.Label(main_frame, text="", foreground="white")
result_label.pack(pady=(15, 5))

# --- Convert Function ---
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

# --- Convert Button ---
convert_btn = ttk.Button(main_frame, text="Convert", command=convert)
convert_btn.pack(pady=(10, 0))

root.mainloop()
