import requests
import json
import os
from bs4 import BeautifulSoup

# Telegram bilgileri (GitHub Secrets'tan gelecek)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Takip edilecek ürün
URL = "https://www.trendyol.com/rampage/zenith-pro-4k-26000-dpi-kablosuz-siyah-gaming-mouse-p-854636160"

# Sadece fiyatın olduğu CSS
PRICE_SELECTOR = "span.prc-dsc"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def telegram_gonder(mesaj):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": mesaj}
    )

def fiyat_cek():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    el = soup.select_one(PRICE_SELECTOR)
    return el.text.strip() if el else None

# Önceki fiyatı oku
try:
    with open("price.json") as f:
        old_price = json.load(f)["price"]
except:
    old_price = None

current_price = fiyat_cek()

if current_price is None:
    print("Fiyat bulunamadı")
    exit()

if old_price and current_price != old_price:
    telegram_gonder(
        f"💰 FİYAT DEĞİŞTİ!\n\nEski: {old_price}\nYeni: {current_price}\n\n{URL}"
    )

# Güncel fiyatı kaydet
with open("price.json", "w") as f:
    json.dump({"price": current_price}, f)
