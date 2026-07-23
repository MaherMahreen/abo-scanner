import os
import requests

def kirim_radar_telegram(pesan):
    """
    Sends radar alert notifications directly to your Telegram bot.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    if not token or not chat_id:
        print("Telegram configuration error: Secrets are missing.")
        return False
        
    url = f"https://telegram.org{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to Telegram API: {e}")
        return False
