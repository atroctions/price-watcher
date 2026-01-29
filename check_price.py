import requests
import json
import os
from bs4 import BeautifulSoup

# ==============================
# TELEGRAM AYARLARI
# ==============================
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==============================
# TELEGRAM MESAJ GÖNDER
# ==============================
def telegram_gonder(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=10
    )

# ==============================
# FİYAT ÇEK
# ==============================
def fiyat_cek(url, selector):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.select_one(selector)
    return el.text.strip() if el else None

# ==============================
# ÜRÜNLERİ OKU
# ==============================
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# ==============================
# ÖNCEKİ FİYATLARI OKU (RUN İÇİ REFERANS)
# ==============================
try:
    with open("prices.json", "r", encoding="utf-8") as f:
        old_prices = json.load(f)
except:
    old_prices = {}

new_prices = {}

# ==============================
# ÜRÜNLERİ KONTROL ET
# ==============================
for p in products:
    product_id = p["id"]
    name = p["name"]
    url = p["url"]
    selector = p["selector"]

    current_price = fiyat_cek(url, selector)
    if not current_price:
        continue

    old_price = old_prices.get(product_id)

    # FİYAT DEĞİŞTİYSE BİLDİR
    if old_price and current_price != old_price:
        telegram_gonder(
            f"💰 FİYAT DEĞİŞTİ\n\n"
            f"{name}\n\n"
            f"Eski: {old_price}\n"
            f"Yeni: {current_price}\n\n"
            f"{url}"
        )

    new_prices[product_id] = current_price

# ==============================
# GÜNCEL FİYATLARI KAYDET
# ==============================
with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(new_prices, f, ensure_ascii=False, indent=2)
