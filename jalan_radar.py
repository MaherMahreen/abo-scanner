import os
import requests

# Mengambil token dan chat ID dari GitHub Secrets Anda
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Pastikan token tidak kosong
if not TOKEN or not CHAT_ID:
    print("❌ ERROR: TELEGRAM_TOKEN atau CHAT_ID di GitHub Secrets belum diisi dengan benar!")
    exit(1)

# Format URL API Telegram yang benar (menggunakan kata 'bot')
url = f"https://telegram.com{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🎉 BERHASIL! GitHub Actions Anda sekarang sudah bisa mengirim pesan ke Telegram."
}

print("Sedang mencoba mengirim pesan ke Telegram...")
response = requests.post(url, json=payload)

print(f"Status Code dari Telegram: {response.status_code}")
print(f"Respon Server: {response.text}")

if response.status_code == 200:
    print("✅ Pesan sukses terkirim! Silakan cek aplikasi Telegram Anda.")
else:
    print("❌ Gagal mengirim pesan. Silakan periksa kembali Token atau Chat ID Anda di GitHub Secrets.")
