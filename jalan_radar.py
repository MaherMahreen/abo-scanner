import os
import pandas as pd
import yfinance as yf
import requests

def hitung_bollinger_squeeze(df, periode=20, std_dev=2):
    if len(df) < periode:
        return None
    df['MA20'] = df['Close'].rolling(window=periode).mean()
    df['STD20'] = df['Close'].rolling(window=periode).std()
    df['Upper'] = df['MA20'] + (std_dev * df['STD20'])
    df['Lower'] = df['MA20'] - (std_dev * df['STD20'])
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    return df
import os
import pandas as pd
import yfinance as yf
import requests

# =====================================================================
# KUNCI SUKSES: MASUKKAN DATA TELEGRAM ANDA LANGSUNG DI BAWAH INI!
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8567909596"
# =====================================================================

def hitung_bollinger_squeeze(df, periode=20, std_dev=2):
    if len(df) < periode:
        return None
    df['MA20'] = df['Close'].rolling(window=periode).mean()
    df['STD20'] = df['Close'].rolling(window=periode).std()
    df['Upper'] = df['MA20'] + (std_dev * df['STD20'])
    df['Lower'] = df['MA20'] - (std_dev * df['STD20'])
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    return df

def kirim_radar_telegram(pesan):
    # Langsung menembak nilai asli tanpa lewat sistem rahasia GitHub lagi
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {"chat_id": str(CHAT_ID_LANGSUNG), "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to Telegram API: {e}")
        return False

def muat_daftar_saham():
    print("✅ Memuat daftar saham utama IHSG untuk tes langsung...")
    return [
        "BBRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "BMRI.JK", 
        "BBNI.JK", "ADRO.JK", "UNVR.JK", "AMRT.JK", "KLBF.JK"
    ]

def jalankan_pemindaian():
    # TEST PING AWAL: Wajib mengirim pesan tanpa saringan untuk tes jembatan
    kirim_radar_telegram("🤖 *ABO Scanner Terhubung Langsung!* Memulai pemindaian bursa harian...")
    
    daftar_saham = muat_daftar_saham()
    print("🚀 Starting technical calculation process...")
    
    sinyal_ditemukan = 0
    for kode_saham in daftar_saham:
        try:
            ticker = yf.Ticker(kode_saham)
            data_historis = ticker.history(period="60d")
            if data_historis.empty or len(data_historis) < 20:
                continue
            df_analisis = hitung_bollinger_squeeze(data_historis)
            if df_analisis is None:
                continue
            
            bandwidth_sekarang = df_analisis['Bandwidth'].iloc[-1]
            harga_sekarang = df_analisis['Close'].iloc[-1]
            min_bandwidth_20h = df_analisis['Bandwidth'].tail(20).min()
            
            # Filter dilonggarkan maksimal agar jaminan notifikasi malam ini keluar banyak
            if bandwidth_sekarang <= 0.60 or bandwidth_sekarang == min_bandwidth_20h:
                volume_sekarang = df_analisis['Volume'].iloc[-1]
                rata_volume_20h = df_analisis['Volume'].tail(20).mean()
                
                status_vol = "Volume Mengering (Konsolidasi)"
                if volume_sekarang > (rata_volume_20h * 1.1):
                    status_vol = "🔥 VOLUME SPIKE! Siap terbang!"
                
                clean_name = kode_saham.replace(".JK", "")
                pesan = (
                    f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                    f"Saham: *{clean_name}*\n"
                    f"Harga: Rp {int(harga_sekarang)}\n"
                    f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                    f"Kondisi: {status_vol}\n\n"
                    f"💡 _Rekomendasi: Pantau harga breakout Upper Band di Rp {int(df_analisis['Upper'].iloc[-1])}_"
                )
                print(f"🎯 Signal found: {clean_name}")
                kirim_radar_telegram(pesan)
                sinyal_ditemukan += 1
        except Exception as err:
            print(f"⚠️ Error reading ticker {kode_saham}: {err}")
            
    kirim_radar_telegram(f"🏁 *Pemindaian Sukses.* Berhasil menemukan {sinyal_ditemukan} saham potensial.")

if __name__ == "__main__":
    jalankan_pemindaian()

def kirim_radar_telegram(pesan):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("Telegram configuration error: Secrets are missing.")
        return False
    url = f"https://telegram.org{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to Telegram API: {e}")
        return False

def muat_daftar_saham():
    print("✅ Memuat daftar saham utama IHSG untuk tes langsung...")
    return [
        "BBRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "BMRI.JK", 
        "BBNI.JK", "ADRO.JK", "UNVR.JK", "AMRT.JK", "KLBF.JK"
    ]

def jalankan_pemindaian():
    # === TES KONEKSI MANDATORI ===
    # Baris ini dipaksa jalan duluan untuk membuktikan token & ID Anda 100% bekerja!
    kirim_radar_telegram("🤖 *ABO Scanner Terhubung!* Memulai pemindaian bursa malam ini...")
    
    daftar_saham = muat_daftar_saham()
    print("🚀 Starting technical calculation process...")
    
    sinyal_ditemukan = 0
    for kode_saham in daftar_saham:
        try:
            ticker = yf.Ticker(kode_saham)
            data_historis = ticker.history(period="60d")
            if data_historis.empty or len(data_historis) < 20:
                continue
            df_analisis = hitung_bollinger_squeeze(data_historis)
            if df_analisis is None:
                continue
            
            bandwidth_sekarang = df_analisis['Bandwidth'].iloc[-1]
            harga_sekarang = df_analisis['Close'].iloc[-1]
            min_bandwidth_20h = df_analisis['Bandwidth'].tail(20).min()
            
            # Saringan dilonggarkan maksimal agar memperbesar peluang lolos
            if bandwidth_sekarang <= 0.60 or bandwidth_sekarang == min_bandwidth_20h:
                volume_sekarang = df_analisis['Volume'].iloc[-1]
                rata_volume_20h = df_analisis['Volume'].tail(20).mean()
                
                status_vol = "Volume Mengering (Konsolidasi)"
                if volume_sekarang > (rata_volume_20h * 1.1):
                    status_vol = "🔥 VOLUME SPIKE! Siap terbang!"
                
                clean_name = kode_saham.replace(".JK", "")
                pesan = (
                    f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                    f"Saham: *{clean_name}*\n"
                    f"Harga: Rp {int(harga_sekarang)}\n"
                    f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                    f"Kondisi: {status_vol}\n\n"
                    f"💡 _Rekomendasi: Pantau harga breakout Upper Band di Rp {int(df_analisis['Upper'].iloc[-1])}_"
                )
                print(f"🎯 Signal found: {clean_name}")
                kirim_radar_telegram(pesan)
                sinyal_ditemukan += 1
        except Exception as err:
            print(f"⚠️ Error reading ticker {kode_saham}: {err}")
            
    # Laporan penutup ke Telegram
    kirim_radar_telegram(f"🏁 *Pemindaian Selesai.* Menemukan {sinyal_ditemukan} saham potensial.")

if __name__ == "__main__":
    jalankan_pemindaian()
