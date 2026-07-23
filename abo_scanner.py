import os
import requests
import yfinance as yf
import pandas as pd

# 1. Konfigurasi Telegram dari GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Daftar saham yang ingin dipantau (contoh saham BBRI, TLKM, ASII, GOTO)
# Untuk pasar Indonesia, gunakan akhiran .JK
SAHAM_WATCHLIST = ["BBRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "BBNI.JK", "BMRI.JK"]

def kirim_telegram(pesan):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Gagal mengirim Telegram: {e}")

def cek_sideways(ticker_symbol):
    # Mengambil data 60 hari bursa terakhir
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="60d")
    
    if len(df) < 20:
        return
    
    # Hitung Bollinger Bands (Periode 20, Standar Deviasi 2)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['STD20'] = df['Close'].rolling(window=20).std()
    df['Upper'] = df['MA20'] + (2 * df['STD20'])
    df['Lower'] = df['MA20'] - (2 * df['STD20'])
    
    # Hitung Persentase Bandwidth (Lebar Band)
    # Semakin kecil nilainya, semakin sideways/menyempit saham tersebut
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    
    # Ambil kondisi terbaru (hari ini)
    bandwidth_sekarang = df['Bandwidth'].iloc[-1]
    harga_sekarang = df['Close'].iloc[-1]
    
    # Cari nilai minimum bandwidth dalam 20 hari terakhir untuk melihat tren penyempitan
    min_bandwidth_20d = df['Bandwidth'].tail(20).min()
    
    # Kriteria Sideways Keras (Bandwidth di bawah 5% atau berada di titik terendahnya)
    # Anda bisa menyesuaikan angka 0.05 (5%) sesuai karakteristik volatilitas saham
    if bandwidth_sekarang <= 0.05 or bandwidth_sekarang == min_bandwidth_20d:
        # Cek apakah volume hari ini mulai naik di atas rata-rata (tanda konfirmasi awal terbang)
        volume_sekarang = df['Volume'].iloc[-1]
        rata_volume = df['Volume'].tail(20).mean()
        
        status_vol = "Volume Kering (Akumulasi)" if volume_sekarang < rata_volume else "Volume Spike (Mulai Terbang!)"
        
        pesan = (
            f"🚨 *RADAR SAHAM SIDEWAYS* 🚨\n\n"
            f"Sinyal ditemukan pada saham: *{ticker_symbol.split('.')[0]}*\n"
            f"Harga Terakhir: Rp {int(harga_sekarang)}\n"
            f"Lebar Bollinger Band: {bandwidth_sekarang*100:.2f}%\n"
            f"Kondisi: {status_vol}\n\n"
            f"💡 _Saham sudah berkonsolidasi lama. Siap-siap pasang buy order jika breakout Upper Band._"
        )
        kirim_telegram(pesan)

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Error: Kredensial Telegram belum diatur di Secrets GitHub.")
    else:
        print("Memulai pemindaian pasar...")
        for saham in SAHAM_WATCHLIST:
            try:
                cek_sideways(saham)
            except Exception as e:
                print(f"Gagal memproses {saham}: {e}")
