import requests

# =====================================================================
# DATA KREDENSIAL ASLI ANDA (SUNTIKAN LANGSUNG)
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8690860489"
# =====================================================================

def kirim_pesan_murni(teks):
    """
    Fungsi super ringan untuk menembak pesan teks langsung tanpa rumus saham.
    """
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID_LANGSUNG),
        "text": teks,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ BERHASIL: Pesan teks murni sukses dikirim ke Telegram!")
            return True
        else:
            print(f"❌ GAGAL: Server Telegram menolak dengan kode {response.status_code}")
            print(f"Respon server: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERROR: Gagal terhubung ke API Telegram: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Memulai pengujian kirim pesan teks murni...")
    
    pesan_tes = (
        "🤖 *NOTIFIKASI AKTIF TANPA SAHAM*\n\n"
        "Hallo Bos! Ini adalah pesan tes murni.\n"
        "Semua rumus saringan saham sudah dimatikan.\n\n"
        "💡 _Jika pesan ini masuk, artinya Token dan ID Anda sudah 100% tepat!_"
    )
    
    kirim_pesan_murni(pesan_tes)
