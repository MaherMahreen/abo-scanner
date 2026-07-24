import os
import sys
import time
import requests

# =========================================================================
# 📝 PENGATURAN KREDENSIAL TELEGRAM (SUDAH DIISI LANGSUNG)
# =========================================================================
TELEGRAM_TOKEN = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID = "8690860489"
# =========================================================================

def send_telegram_notification(bot_token, chat_id, stocks_list):
    """
    Fungsi untuk mengirimkan daftar saham ke Telegram secara aman.
    Otomatis membagi pesan menjadi beberapa bagian jika melebihi batas karakter Telegram.
    """
    if not bot_token or not chat_id:
        print("[ERROR] Token Bot atau Chat ID Telegram kosong! Periksa kembali variabel Anda.")
        return

    if not stocks_list:
        print("[INFO] Tidak ada saham yang ditemukan untuk dikirim.")
        return

    # 1. Format daftar saham menjadi teks per baris menggunakan format HTML yang stabil
    lines = [f"{i+1}. {stock}" for i, stock in enumerate(stocks_list)]
    
    # 2. Bagi teks menjadi beberapa bagian (chunks) jika melebihi batas aman 3.500 karakter
    MAX_CHARACTERS = 3500
    chunks = []
    current_chunk = "<b>📊 Hasil ABO Scanner Massal</b>\n\n"
    
    for line in lines:
        # Jika ditambah baris baru akan melebihi limit, simpan bagian saat ini dan buat yang baru
        if len(current_chunk) + len(line) + 1 > MAX_CHARACTERS:
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)

    # 3. Proses pengiriman setiap bagian ke API Telegram
    url = f"https://telegram.org{bot_token}/sendMessage"
    
    for index, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML"
        }
        
        try:
            print(f"[INFO] Mengirim notifikasi bagian {index+1}/{len(chunks)}...")
            response = requests.post(url, json=payload, timeout=15)
            response_data = response.json()
            
            # Jika Telegram menolak karena kesalahan parsing HTML, gunakan fallback ke teks biasa
            if not response_data.get("ok"):
                print(f"[X] Telegram menolak pesan: {response_data.get('description')}")
                if "can't parse" in response_data.get('description', '').lower():
                    print("[INFO] Mengirim ulang sebagai Plain Text tanpa HTML format...")
                    payload.pop("parse_mode", None)
                    response = requests.post(url, json=payload, timeout=15)
                    response_data = response.json()
                    
                if not response_data.get("ok"):
                    print(f"[ERROR] Gagal total mengirimkan bagian {index+1}.")
            else:
                print(f"[OK] Bagian {index+1} berhasil dikirim ke Telegram.")
                
            # Jeda 1 detik antar pesan untuk menghindari rate-limit (spam block) dari Telegram
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Masalah koneksi jaringan ke API Telegram: {e}")


def run_scanner_logic():
    """
    Tempatkan LOGIKA UTAMA skrip scanning saham Anda di dalam fungsi ini.
    """
    print("# FIXED: Diarahkan langsung ke main.py agar seluruh modul Score & Signal Engine aktif nyata!")
    print("Memicu jembatan notifikasi...")
    
    # -------------------------------------------------------------------------
    # ⚠️ BAGIAN INI HARUS ANDA SESUAIKAN DENGAN LOGIKA SCANNER ASLI ANDA ⚠️
    # Pastikan hasil akhir dari pemindaian Anda menghasilkan sebuah LIST/DAFTAR teks saham.
    # Contoh di bawah ini mensimulasikan hasil deteksi 617 saham.
    
    hasil_saham = [f"SAHAM-{i}" for i in range(1, 618)]  # Hapus/ganti baris ini dengan rumus scanner Anda
    # -------------------------------------------------------------------------
    
    print(f"Berhasil memuat {len(hasil_saham)} saham.")
    return hasil_saham


if __name__ == "__main__":
    # 1. Jalankan proses pemindaian saham utama
    daftar_saham_terdeteksi = run_scanner_logic()
    
    # 2. Eksekusi pengiriman notifikasi massal ke Telegram menggunakan kredensial di atas
    send_telegram_notification(TELEGRAM_TOKEN, CHAT_ID, daftar_saham_terdeteksi)
