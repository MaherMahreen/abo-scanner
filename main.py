import os
import requests
import re
import time
from saham_syariah import DAFTAR_SAHAM_SYARIAH
from score import ScoreEngine

TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID_LANGSUNG = "8690860489"

# =====================================================================
# KONFIGURASI PARAMETER TRADING AMAN (ADAPTASI DARI config.py)
# =====================================================================
SIDEWAYS_RANGE = 0.15          # Toleransi lebar bandwidth sideways maks 15%
BREAKOUT_LOOKBACK = 20         # Melihat batas tertinggi harga 20 hari ke belakang
VOLUME_SPIKE_RATIO = 1.3       # Volume hari ini wajib 1.3x lipat rata-rata
MIN_VALUE_TRANSACTION = 500000000 # Minimal nilai transaksi harian Rp 500 Juta (Likuid)
# =====================================================================

def kirim_radar_telegram(pesan):
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {"chat_id": str(CHAT_ID_LANGSUNG), "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def hitung_ema(prices, periode):
    """Menghitung Exponential Moving Average secara murni matematika tanpa pandas"""
    if len(prices) < periode:
        return 0
    k = 2 / (periode + 1)
    ema_val = sum(prices[:periode]) / periode
    for price in prices[periode:]:
        ema_val = (price * k) + (ema_val * (1 - k))
    return ema_val

def cek_sideways_dan_sinyal(ticker_clean, engine):
    ticker_jk = f"{ticker_clean}.JK"
    url = f"https://yahoo.com{ticker_jk}?range=30d&interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    time.sleep(0.4) # Jeda aman anti-blokir bursa
    engine.reset()  # Reset mesin skor untuk saham baru
    
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
        
        if len(prices) < 20 or len(volumes) < 20:
            return None
            
        harga_sekarang = prices[-1]
        volume_sekarang = volumes[-1]
        
        # 1. EVALUASI ATURAN TRANSAKSI (Filter Likuiditas Rp 500 Juta)
        nilai_transaksi_hari_ini = harga_sekarang * volume_sekarang
        if nilai_transaksi_hari_ini < MIN_VALUE_TRANSACTION:
            return None # Lempar senyap jika sahamnya tidak likuid/saham tidur
            
        # Perhitungan indikator dasar Bollinger Bands
        close_20d = prices[-20:]
        ma20 = sum(close_20d) / 20
        variance = sum((x - ma20) ** 2 for x in close_20d) / 20
        std_dev = variance ** 0.5
        upper_band = ma20 + (2 * std_dev)
        lower_band = ma20 - (2 * std_dev)
        bandwidth_sekarang = (upper_band - lower_band) / ma20 if ma20 != 0 else 0
        
        # 2. EVALUASI ATURAN SIDEWAYS (Maks 15%)
        if bandwidth_sekarang <= 0.08:
            engine.tambah(35, "Sideways Super Ketat (Squeeze Ekstrem)")
        elif bandwidth_sekarang <= SIDEWAYS_RANGE:
            engine.tambah(20, "Sideways Normal (Konsolidasi)")
        else:
            return None # Lewati jika volatilitas melebar kencang
            
        # 3. EVALUASI ATURAN BREAKOUT
        harga_tertinggi_bursa = max(prices[-(BREAKOUT_LOOKBACK+1):-1])
        if harga_sekarang > harga_tertinggi_bursa:
            engine.tambah(25, "BREAKOUT HIGH! Menembus Resistance Kuat")
        elif harga_sekarang >= upper_band:
            engine.tambah(15, "Breakout Upper Band (Awal Konfirmasi Terbang)")
            
        # 4. EVALUASI ATURAN VOLUME SPIKE
        rata_volume_20h = sum(volumes[-20:]) / 20
        if volume_sekarang > (rata_volume_20h * 2.0):
            engine.tambah(25, "VOLUME SPIKE EKSTREM! Bandar Borong Besar-Besaran")
        elif volume_sekarang > (rata_volume_20h * VOLUME_SPIKE_RATIO):
            engine.tambah(15, "Volume Spike Normal (Akumulasi Awal)")
            
        # 5. EVALUASI ATURAN EMA TREND (EMA Cepat > EMA Lambat)
        ema20 = hitung_ema(prices, 20)
        ema30 = hitung_ema(prices, 30) # Cadangan filter tren lambat
        if ema20 > b"" and ema20 > ema30:
            engine.tambah(15, "EMA Golden Cross (Tren Bullish Menguat)")
            
        data_skor = engine.hasil()
        
        return {
            "ticker": ticker_clean,
            "harga": int(harga_sekarang),
            "bandwidth": bandwidth_sekarang * 100,
            "score": data_skor["score"],
            "alasan": " \n├ ⚡ " + " \n├ ⚡ ".join(data_skor["alasan"]),
            "target": int(upper_band)
        }
    except Exception:
        return None

if __name__ == "__main__":
    kirim_radar_telegram("🤖 *ABO Scanner Pro v1.5 Online!* Memulai pemindaian massal menggunakan Signal & Score Engine gabungan...")
    
    engine = ScoreEngine()
    hasil_scan = []
    
    daftar_saham = muat_saham_dari_csv() if 'muat_saham_dari_csv' in locals() else DAFTAR_SAHAM_SYARIAH
    print(f"Memulai kalkulasi {len(daftar_saham)} saham syariah...")
    
    for ticker in daftar_saham:
        res = cek_sideways_and_sinyal(ticker.strip().upper(), engine)
        if res is not None:
            hasil_scan.append(res)
            
    # Mengurutkan hasil berdasarkan ABO Score Tertinggi
    hasil_scan.sort(key=lambda x: x["score"], reverse=True)
    top_20 = hasil_scan[:20]
    
    if top_20:
        for i, saham in enumerate(top_20, 1):
            pesan = (
                f"🏆 *RANK #{i}: {saham['ticker']}* (ABO Score: {saham['score']}/100)\n"
                f"Harga Terakhir: Rp {saham['harga']} | Bandwidth: {saham['bandwidth']:.2f}%\n"
                f"📋 *Sinyal Indikator Terdeteksi:*{saham['alasan']}\n\n"
                f"💡 _Breakout Resistance Target: Rp {saham['target']}_\n"
                f"━━━━━━━⚙️ ABO PRO ENGINE ⚙️━━━━━━━"
            )
            kirim_radar_telegram(pesan)
    else:
        kirim_radar_telegram("ℹ️ Pemindaian selesai. Tidak ada saham syariah likuid yang masuk radar hari ini.")
        
    kirim_radar_telegram("🏁 *ABO Pro Scanner Selesai.* Laporan sinyal trading berhasil diperbarui.")
