import os
import requests
import re
import time
from score import ScoreEngine

TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc"
CHAT_ID_LANGSUNG = "8690860489"

def kirim_radar_telegram(pesan):
    url = f"https://api.telegram.org/bot8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc/sendMessage"
    payload = {"chat_id": str("8690860489"), "text": pesan}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def muat_saham_dari_csv():
    nama_file = "saham_syariah.csv"
    if not os.path.exists(nama_file): return []
    clean_tickers = []
    try:
        with open(nama_file, "r") as f:
            lines = f.readlines()
        for line in lines:
            ticker = line.strip().upper()
            if ticker in ["", "KODE", "TICKER"]: continue
            clean_tickers.append(ticker)
        return clean_tickers
    except Exception: return []

def cek_sideways_yahoo(ticker_clean, engine):
    ticker_jk = f"{ticker_clean}.JK"
    url = f"https://yahoo.com{ticker_jk}?range=30d&interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    time.sleep(0.4)
    engine.reset()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: return
        teks_data = response.text
        pola_harga = r'"close":\[([^[\]]+)\]'
        cari_harga = re.search(pola_harga, teks_data)
        if not cari_harga: return
        prices = [float(x) for x in cari_harga.group(1).split(',') if x != 'null']
        if len(prices) < 20: return
        harga_sekarang = prices[-1]
        
        pesan = f"🚨 RADAR SAHAM: {ticker_clean} | Harga: Rp {int(harga_sekarang)}"
        print(f"Sinyal: {ticker_clean}")
        kirim_radar_telegram(pesan)
    except Exception: pass

if __name__ == "__main__":
    kirim_radar_telegram("🤖 ABO Scanner Backup Aktif dengan Token Baru!")
    engine = ScoreEngine()
    daftar_saham = muat_saham_dari_csv()
    for ticker in daftar_saham[:5]: # Membatasi 5 saham saja untuk tes cepat jalan_radar
        cek_sideways_yahoo(ticker, engine)
