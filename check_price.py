import requests
import json
import os
from bs4 import BeautifulSoup

# 🔐 Telegram bilgileri (GitHub Secrets'tan gelir)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def telegram_gonder(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        }
    )

def fiyat_cek(url, selector):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.select_one(selector)
    return el.text.strip() if el else None


# 🧪 TEST MESAJI — SADECE TEST İÇİN
telegram_gonder("🧪 TEST MESAJI: Sistem çalışıyor")


# 📦 Ürün listesini oku
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# 🔁 Geçici referanslar (run içi)
old_prices = {}
new_prices = {}

for p in products:
    current_price = fiyat_cek(p["url"], p["selector"])
    if not current_price:
        continue

    new_prices[p["id"]] = current_price
