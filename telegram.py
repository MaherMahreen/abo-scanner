import requests

TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc"
CHAT_ID_LANGSUNG = "8690860489"

def kirim_radar_telegram(pesan):
    url = f"https://api.telegram.org/bot8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc/sendMessage"
    payload = {
        "chat_id": str("8690860489"),
        "text": pesan
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False
