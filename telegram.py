import requests

TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID_LANGSUNG = "8690860489"

def kirim_radar_telegram(pesan):
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID_LANGSUNG),
        "text": pesan
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False
