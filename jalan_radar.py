import os
import requests
import re
import time
# MEMANGGIL DATA 618 SAHAM DARI FILE SAHAM_SYARIAH.PY SECARA OTOMATIS
from saham_syariah import DAFTAR_SAHAM_SYARIAH

# =====================================================================
# DATA KREDENSIAL UTUH (SUDAH DIKUNCI DAN VALID)
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8690860489"
# =====================================================================

def kirim_radar_telegram(pesan):
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {"chat_id": str(CHAT_ID_LANGSUNG), "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")
        return False

def cek_sideways_yahoo(ticker_clean):
    ticker_jk = f"{ticker_clean}.JK"
    url = f"https://yahoo.com{ticker_jk}?range=30d&interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Jeda aman 0.4 detik agar tidak diblokir Yahoo Finance
    time.sleep(0.4)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return
            
        teks_data = response.text
        
        pola_harga = r'"close":\[([^[\]]+)\]'
        pola_volume = r'"volume":\[([^[\]]+)\]'
        
        cari_harga = re.search(pola_harga, teks_data)
        cari_volume = re.search(pola_volume, teks_data)
        
        if not cari_harga or not cari_volume:
            return
            
        prices = [float(x) for x in cari_harga.group(1).split(',') if x != 'null']
        volumes = [float(v) for v in cari_volume.group(1).split(',') if v != 'null']
        
        if len(prices) < 20:
            return
            
        close_20d = prices[-20:]
        ma20 = sum(close_20d) / 20
        
        variance = sum((x - ma20) ** 2 for x in close_20d) / 20
        std_dev = variance ** 0.5
        
        upper_band = ma20 + (2 * std_dev)
        lower_band = ma20 - (2 * std_dev)
        
        harga_sekarang = prices[-1]
        bandwidth_sekarang = (upper_band - lower_band) / ma20 if ma20 != 0 else 0
        
        # Saringan real trading diperketat ke 0.15 agar hanya saham sideways keras kualitas A yang masuk radar
        if bandwidth_sekarang <= 0.15: 
            volume_sekarang = volumes[-1] if volumes else 0
            rata_volume = sum(volumes[-20:]) / 20 if volumes else 1
            
            status_vol = "Volume Mengering"
            if volume_sekarang > (rata_volume * 1.3):
                status_vol = "VOLUME SPIKE! Bandar Masuk!"
                
            pesan = (
                f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                f"Saham Syariah: *{ticker_clean}*\n"
                f"Harga Terakhir: Rp {int(harga_sekarang)}\n"
                f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                f"Kondisi: {status_vol}\n\n"
                f"💡 _Breakout Target: Rp {int(upper_band)}_"
            )
            print(f"🎯 Sinyal Ditemukan: {ticker_clean}")
            kirim_radar_telegram(pesan)
            
    except Exception as e:
        print(f"Skip {ticker_clean}: {e}")

if __name__ == "__main__":
    print("Memicu jembatan notifikasi...")
    kirim_radar_telegram("🤖 *ABO Scanner Massal Aktif!* Memulai penyaringan aman pada 618 saham syariah...")
    
    for ticker in DAFTAR_SAHAM_SYARIAH:
        cek_sideways_yahoo(ticker.strip().upper())
        
    kirim_radar_telegram("🏁 Pemindaian Selesai. Semua saham syariah selesai disaring.")
