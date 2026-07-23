import os
import requests
import re
import time
from saham_syariah import DAFTAR_SAHAM_SYARIAH
from score import ScoreEngine  # MEMANGGIL MESIN SKOR ANDA

TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID_LANGSUNG = "8690860489"

def kirim_radar_telegram(pesan):
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {"chat_id": str(CHAT_ID_LANGSUNG), "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def cek_sideways_yahoo(ticker_clean, engine):
    ticker_jk = f"{ticker_clean}.JK"
    url = f"https://yahoo.com{ticker_jk}?range=30d&interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    time.sleep(0.4) # Jeda aman anti-blokir
    engine.reset()  # Reset skor untuk saham baru
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        teks_data = response.text
        pola_harga = r'"close":\[([^[\]]+)\]'
        pola_volume = r'"volume":\[([^[\]]+)\]'
        
        cari_harga = re.search(pola_harga, teks_data)
        cari_volume = re.search(pola_volume, teks_data)
        
        if not cari_harga or not cari_volume:
            return None
            
        prices = [float(x) for x in cari_harga.group(1).split(',') if x != 'null']
        volumes = [float(v) for v in cari_volume.group(1).split(',') if v != 'null']
        
        if len(prices) < 20:
            return None
            
        close_20d = prices[-20:]
        ma20 = sum(close_20d) / 20
        variance = sum((x - ma20) ** 2 for x in close_20d) / 20
        std_dev = variance ** 0.5
        upper_band = ma20 + (2 * std_dev)
        lower_band = ma20 - (2 * std_dev)
        
        harga_sekarang = prices[-1]
        bandwidth_sekarang = (upper_band - lower_band) / ma20 if ma20 != 0 else 0
        
        # =====================================================================
        # ENGINE SKORING ATURAN TRADING (ABO SCORE ENGINE)
        # =====================================================================
        # Aturan 1: Ketatnya Sideways (Max 40 Poin)
        if bandwidth_sekarang <= 0.08:
            engine.tambah(40, "Sideways Super Ketat (Squeeze Ekstrem)")
        elif bandwidth_sekarang <= 0.15:
            engine.tambah(25, "Sideways Normal (Konsolidasi)")
        else:
            return None # Skip jika volatilitas terlalu lebar/tidak sideways
            
        # Aturan 2: Deteksi Volume Spike (Max 40 Poin)
        volume_sekarang = volumes[-1] if volumes else 0
        rata_volume = sum(volumes[-20:]) / 20 if volumes else 1
        if volume_sekarang > (rata_volume * 2.0):
            engine.tambah(40, "Volume Spike Ekstrem (Ledakan Volume Bandar)")
        elif volume_sekarang > (rata_volume * 1.3):
            engine.tambah(20, "Volume Spike Normal (Akumulasi Awal)")
        else:
            engine.tambah(5, "Volume Mengering (Fase Pengumpulan)")
            
        # Aturan 3: Posisi Harga terhadap MA20 (Max 20 Poin)
        if harga_sekarang > ma20:
            engine.tambah(20, "Harga di atas MA20 (Tren Bullish Pendek)")
        else:
            engine.tambah(5, "Harga di bawah MA20 (Fase Bottoming)")
            
        # Ambil hasil akhir skor dari score.py
        data_skor = engine.hasil()
        
        return {
            "ticker": ticker_clean,
            "harga": int(harga_sekarang),
            "bandwidth": bandwidth_sekarang * 100,
            "score": data_skor["score"],
            "alasan": ", ".join(data_skor["alasan"]),
            "target": int(upper_band)
        }
    except Exception:
        return None

if __name__ == "__main__":
    kirim_radar_telegram("🤖 *ABO Scanner v1.0 Aktif!* Memulai pemindaian dan penilaian ABO Score pada saham syariah...")
    
    engine = ScoreEngine() # Menyalakan mesin skor
    hasil_scan = []
    
    for ticker in DAFTAR_SAHAM_SYARIAH:
        res = cek_sideways_yahoo(ticker.strip().upper(), engine)
        if res is not None:
            hasil_scan.append(res)
            
    # Mengurutkan hasil scan berdasarkan ABO Score tertinggi (Ranking Top 20)
    hasil_scan.sort(key=lambda x: x["score"], reverse=True)
    top_20 = hasil_scan[:20]
    
    # Kirim hasil peringkat ke Telegram
    if top_20:
        for i, saham in enumerate(top_20, 1):
            pesan = (
                f"🏆 *RANK #{i}: {saham['ticker']}* (ABO Score: {saham['score']}/100)\n\n"
                f"Harga Terakhir: Rp {saham['harga']}\n"
                f"Lebar Bandwidth: {saham['bandwidth']:.2f}%\n"
                f"Analisis: {saham['alasan']}\n\n"
                f"💡 _Breakout Target: Rp {saham['target']}_"
            )
            kirim_radar_telegram(pesan)
    else:
        kirim_radar_telegram("ℹ️ Pemindaian selesai. Tidak ada saham syariah yang masuk kriteria sideways hari ini.")
        
    kirim_radar_telegram("🏁 *ABO Score Engine Selesai.* Seluruh peringkat Top 20 sukses dikirim.")
