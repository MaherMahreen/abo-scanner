import requests

# =====================================================================
# FIXED TOTAL: ALAMAT JALUR API DAN DATA KREDENSIAL DIKUNCI AMAN
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID_LANGSUNG = "8690860489"
# =====================================================================

def kirim_radar_telegram(pesan):
    """
    Sends radar alert notifications directly to your Telegram bot.
    """
    # Memperbaiki total URL API yang hancur sebelumnya
    url = f"https://telegram.org/bot8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4/sendMessage"
    payload = {
        "chat_id": str("8690860489"),
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Notifikasi modul telegram.py berhasil terkirim!")
            return True
        else:
            print(f"❌ Server Telegram menolak dengan kode status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Telegram API: {e}")
        return False
