import requests
import json
import os
from bs4 import BeautifulSoup

telegram_gonder("🧪 TEST MESAJI: Sistem çalışıyor")


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def telegram_gonder(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": mesaj}
    )

def fiyat_cek(url, selector):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.select_one(selector)
    return el.text.strip() if el else None

# Ürün listesini oku
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Önceki fiyatlar
try:
    with open("prices.json", "r", encoding="utf-8") as f:
        old_prices = json.load(f)
except:
    old_prices = {}

new_prices = {}

for p in products:
    current_price = fiyat_cek(p["url"], p["selector"])
    if not current_price:
        continue

    pid = p["id"]
    old_price = old_prices.get(pid)

    if old_price and current_price != old_price:
        telegram_gonder(
            f"💰 FİYAT DEĞİŞTİ\n\n"
            f"{p['name']}\n\n"
            f"Eski: {old_price}\n"
            f"Yeni: {current_price}\n\n"
            f"{p['url']}"
        )

    new_prices[pid] = current_price

# Güncel fiyatları kaydet
with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(new_prices, f, ensure_ascii=False, indent=2)

print("=== REFERANS FİYATLAR ===")
print(old_prices)
print("=== GÜNCEL FİYATLAR ===")
print(new_prices)

print("=== REFERANS FİYATLAR (OLD) ===")
print(old_prices)

print("=== GÜNCEL FİYATLAR (NEW) ===")
print(new_prices)
