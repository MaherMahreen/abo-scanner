import urllib.request
import json
import re

# =====================================================================
# DATA KREDENSIAL UTUH (SUDAH DIKUNCI DAN VALID)
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8690860489"

# =====================================================================
# SILAKAN MASUKKAN/TEMPEL 618 KODE SAHAM ANDA DI BAWAH INI (CONTOH FORMAT)
# =====================================================================
DAFTAR_SAHAM_SYARIAH = [
    "BBRI", "TLKM", "ASII", "GOTO", "BRIS", "ADRO", "PTBA", "ANTM"
    # ... Sila tambahkan seluruh 618 kode saham Anda di sini tanpa akhiran .JK
]
# =====================================================================

def kirim_radar_telegram(pesan):
    # Menggunakan pustaka bawaan urllib agar 100% bebas error request/pandas
    pesan_encoded = urllib.parse.quote(pesan)
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage?chat_id={CHAT_ID_LANGSUNG}&text={pesan_encoded}&parse_mode=Markdown"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")
        return False

def cek_sideways_yahoo(ticker_clean):
    ticker_jk = f"{ticker_clean}.JK"
    # Mengambil data harga historis mentah langsung dari API Yahoo Finance
    url = f"https://yahoo.com{ticker_jk}?range=60d&interval=1d"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']
        
        # Bersihkan data dari nilai Kosong (None)
        prices = [p for p in prices if p is not None]
        volumes = [v for v in volumes if v is not None]
        
        if len(prices) < 20:
            return
            
        # Hitung Moving Average 20 hari terakhir
        close_20d = prices[-20:]
        ma20 = sum(close_20d) / 20
        
        # Hitung Standar Deviasi murni matematika
        variance = sum((x - ma20) ** 2 for x in close_20d) / 20
        std_dev = variance ** 0.5
        
        upper_band = ma20 + (2 * std_dev)
        lower_band = ma20 - (2 * std_dev)
        
        # Ambil nilai penutupan terakhir
        harga_sekarang = prices[-1]
        bandwidth_sekarang = (upper_band - lower_band) / ma20 if ma20 != 0 else 0
        
        # Kriteria filter sideways dilonggarkan ke 0.40 agar 618 saham Anda banyak yang lolos
        if bandwidth_sekarang <= 0.40:
            volume_sekarang = volumes[-1]
            rata_volume = sum(volumes[-20:]) / 20
            
            status_vol = "Volume Mengering (Konsolidasi)"
            if volume_sekarang > (rata_volume * 1.2):
                status_vol = "🔥 VOLUME SPIKE! Siap terbang!"
                
            pesan = (
                f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                f"Saham Syariah: *{ticker_clean}*\n"
                f"Harga Terakhir: Rp {int(harga_sekarang)}\n"
                f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                f"Kondisi: {status_vol}\n\n"
                f"💡 _Pantau breakout Upper Band di Rp {int(upper_band)}_"
            )
            print(f"🎯 Sinyal Ditemukan: {ticker_clean}")
            kirim_radar_telegram(pesan)
            
    except Exception as err:
        print(f"Lewati {ticker_clean}: {err}")

if __name__ == "__main__":
    kirim_radar_telegram("🤖 *ABO Scanner Massal Aktif!* Mulai memindai 618 saham syariah Anda...")
    
    clean_tickers = []
    for s in DAFTAR_SAHAM_SYARIAH:
        t = s.strip().upper().replace(".JK", "")
        if t != "":
            clean_tickers.append(t)
            
    print(f"Memulai kalkulasi {len(clean_tickers)} saham syariah...")
    for ticker in clean_tickers:
        cek_sideways_yahoo(ticker)
        
    kirim_radar_telegram("🏁 *Pemindaian Selesai.* Semua saham syariah selesai disaring.")
