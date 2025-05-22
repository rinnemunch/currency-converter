import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import requests
from datetime import datetime
from PIL import Image, ImageTk
import io
import os
from dotenv import load_dotenv
import pyperclip


# --- API Setup ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

# --- Currency to Country Mapping ---
from currency_to_country_full import currency_to_country

# --- Flag Functions ---
flag_cache = {}

def get_flag_image(currency_code):
    country_code = currency_to_country.get(currency_code)
    if not country_code:
        return None
    url = f"https://flagcdn.com/32x24/{country_code.lower()}.png"
    try:
        response = requests.get(url)
        img_data = response.content
        image = Image.open(io.BytesIO(img_data)).resize((32, 24))
        return ImageTk.PhotoImage(image)
    except:
        return None

def load_flag(currency_code):
    if currency_code in flag_cache:
        return flag_cache[currency_code]
    img = get_flag_image(currency_code)
    if img:
        flag_cache[currency_code] = img
    return img

def update_flags(*args):
    from_img = load_flag(base_currency.get())
    to_img = load_flag(target_currency.get())
    if from_img:
        from_flag.config(image=from_img)
        from_flag.image = from_img
    if to_img:
        to_flag.config(image=to_img)
        to_flag.image = to_img

def get_currency_list(base="USD"):
    url = BASE_URL + base
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['result'] == 'success':
        return list(data['conversion_rates'].keys())
    else:
        return []

def swap_currencies():
    base = base_currency.get()
    target = target_currency.get()
    base_currency.set(target)
    target_currency.set(base)
    update_flags()

def copy_result():
    result = result_label.cget("text")
    if result:
        pyperclip.copy(result)
        messagebox.showinfo("Copied", "Result copied to clipboard!")


# --- UI Setup ---
BG_COLOR = "white"
BADGE_BG = "#001f4d"

root = tk.Tk()
root.configure(bg=BG_COLOR)
icon = PhotoImage(file="my_icon.png")
root.iconphoto(True, icon)
root.title("PocketRates")
root.geometry("420x710")
root.resizable(False, False)

# --- Style ---
style = ttk.Style()

style.configure("Custom.TFrame", background=BG_COLOR)

style.configure("TLabel",
    font=("Segoe UI", 11),
    background=BG_COLOR,
    foreground="white"
)

style.configure("TButton",
    font=("Segoe UI", 10),
    padding=6
)

style.configure("Custom.TCombobox",
    font=("Segoe UI", 11),
    padding=5,
    foreground="#222",
    fieldbackground="white",
    background="white",
    relief="flat"
)

style.configure("Custom.TEntry",
    font=("Segoe UI", 11),
    padding=5,
    foreground="#222",
    fieldbackground="white",
    background="white",
    relief="flat"
)



# --- Header ---
logo_img = PhotoImage(file="my_icon.png").subsample(13, 13)
header_color = "#001f4d"
header_frame = tk.Frame(root, bg=header_color, height=70)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

app_name = tk.Label(header_frame, text="PocketRates", fg="white", bg=header_color, font=("Segoe UI", 13, "bold"))
app_name.pack(side="left", padx=15)

center_frame = tk.Frame(header_frame, bg=header_color)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

logo_label = tk.Label(center_frame, image=logo_img, bg=header_color)
logo_label.image = logo_img
logo_label.pack(side="left", pady=5, padx=(0, 6))

info_label = tk.Label(header_frame, text="v1.2", fg="white", bg=header_color, font=("Segoe UI", 10))
info_label.pack(side="right", padx=15)

# --- Main Frame ---
main_frame = ttk.Frame(root, padding=20, style="Custom.TFrame")
main_frame.pack(expand=True)

title = ttk.Label(main_frame, text="PocketRates", foreground="black", font=("Segoe UI", 16, "bold"))
title.pack(pady=(0, 20))

currencies = get_currency_list()

# --- From Currency ---
ttk.Label(main_frame, text="From:", foreground="black").pack(pady=(5, 0))
base_currency = ttk.Combobox(main_frame, values=currencies, state="readonly", width=20, style="Custom.TCombobox")
base_currency.set("USD")
base_currency.pack(pady=5)
from_flag = tk.Label(main_frame, bg=BG_COLOR)
from_flag.pack(pady=(0, 5))

# --- To Currency ---
ttk.Label(main_frame, text="To:", foreground="black").pack(pady=(10, 0))
target_currency = ttk.Combobox(main_frame, values=currencies, state="readonly", width=20, style="Custom.TCombobox")
target_currency.set("EUR")
target_currency.pack(pady=5)
to_flag = tk.Label(main_frame, bg=BG_COLOR)
to_flag.pack(pady=(0, 5))

swap_btn = ttk.Button(main_frame, text="Swap", command=swap_currencies)
swap_btn.pack(pady=(5, 5))


# --- Amount ---
ttk.Label(main_frame, text="Amount:", foreground="black").pack(pady=(10, 0))
amount_entry = ttk.Entry(main_frame, width=22, style="Custom.TEntry")
amount_entry.pack(pady=5)

# --- Result Label ---
result_label = ttk.Label(main_frame, text="", foreground="black")
result_label.pack(pady=(15, 5))

copy_btn = ttk.Button(main_frame, text="Copy Result", command=copy_result)
copy_btn.pack(pady=(5, 0))

# --- Convert Button ---
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

convert_btn = ttk.Button(main_frame, text="Convert", command=convert)
convert_btn.pack(pady=(10, 0))

# --- Bind Flag Update ---
base_currency.bind("<<ComboboxSelected>>", update_flags)
target_currency.bind("<<ComboboxSelected>>", update_flags)
update_flags()  # Initial flags

# --- Credits Frame ---
credit_frame = tk.Frame(root, bg=BADGE_BG, height=20)
credit_frame.pack(fill="x")

credit_label = tk.Label(
    credit_frame,
    text="© 2025 PocketRates by Shaun Fulton",
    bg=BADGE_BG,
    fg="white",
    font=("Segoe UI", 8)
)
credit_label.pack(pady=(0, 2))

# --- Footer Frame ---
footer_frame = tk.Frame(root, bg=BADGE_BG, height=70)
footer_frame.pack(fill="x")
footer_frame.pack_propagate(False)

# Subframes
left_side = tk.Frame(footer_frame, bg=BADGE_BG)
left_side.pack(side="left", fill="y", anchor="w")

center_side = tk.Frame(footer_frame, bg=BADGE_BG)
center_side.pack(side="left", expand=True)

right_side = tk.Frame(footer_frame, bg=BADGE_BG)
right_side.pack(side="right", padx=(0, 20), fill="y")

# Apple icon
if os.path.exists("app_store_badge.png"):
    app_store_badge = PhotoImage(file="app_store_badge.png").subsample(5, 5)
    app_store_label = tk.Label(left_side, image=app_store_badge, bg=BADGE_BG)
    app_store_label.image = app_store_badge
    app_store_label.pack(side="left", padx=10, pady=10, anchor="w")

# 5 stars
if os.path.exists("5Stars.png"):
    five_star_img = PhotoImage(file="5Stars.png").subsample(3, 3)
    five_star_label = tk.Label(center_side, image=five_star_img, bg=BADGE_BG)
    five_star_label.image = five_star_img
    five_star_label.pack(pady=10)

# Google Play
if os.path.exists("google_play_badge.png"):
    google_play_badge = PhotoImage(file="google_play_badge.png").subsample(5, 5)
    google_play_label = tk.Label(right_side, image=google_play_badge, bg=BADGE_BG)
    google_play_label.image = google_play_badge
    google_play_label.pack(side="right", pady=10)

root.bind('<Return>', lambda event: convert())
root.mainloop()
