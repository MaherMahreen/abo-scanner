import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": pesan
    }
    requests.post(url, data=data)

kirim_telegram("✅ ABO Scanner aktif. GitHub berhasil terhubung ke Telegram!")
