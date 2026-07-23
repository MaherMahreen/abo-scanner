import os
import requests

def kirim_radar_telegram(pesan):
    """
    Mengirimkan teks notifikasi langsung ke akun/grup Telegram Anda.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    if not token or not chat_id:
        print("Gagal Kirim: Kredensial Telegram Secrets belum diisi di GitHub.")
        return False
        
    url = f"https://telegram.org{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        respon = requests.post(url, json=payload, timeout=10)
        return respon.status_code == 200
    except Exception as e:
        print(f"Error koneksi ke Telegram Telegram: {e}")
        return False
