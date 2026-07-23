import os
import pandas as pd
import yfinance as yf
import requests

def hitung_bollinger_squeeze(df, periode=20, std_dev=2):
    """
    Menghitung penyempitan Bollinger Bands untuk mendeteksi fase sideways.
    """
    if len(df) < periode:
        return None
        
    df['MA20'] = df['Close'].rolling(window=periode).mean()
    df['STD20'] = df['Close'].rolling(window=periode).std()
    
    df['Upper'] = df['MA20'] + (std_dev * df['STD20'])
    df['Lower'] = df['MA20'] - (std_dev * df['STD20'])
    
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    return df

def kirim_radar_telegram(pesan):
    """
    Mengirimkan teks notifikasi langsung ke akun/grup Telegram Anda.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    if not token or not chat_id:
        print("Telegram configuration error: Secrets are missing.")
        return False
        
    url = f"https://telegram.org{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to Telegram API: {e}")
        return False

def muat_daftar_saham():
    nama_file = "saham_syariah.csv"
    if not os.path.exists(nama_file):
        print(f"⚠️ Warning: {nama_file} not found! Using fallback list.")
        return ["BBRI.JK", "TLKM.JK", "ASII.JK"]
        
    try:
        df_saham = pd.read_csv(nama_file)
        print(f"📊 Columns detected in CSV: {list(df_saham.columns)}")
        
        kolom_utama = df_saham.columns[0]
        list_saham = df_saham[kolom_utama].dropna().astype(str).tolist()
        
        list_clean = []
        for s in list_saham:
            s_clean = s.strip().upper()
            if s_clean == "" or "KODE" in s_clean or "TICKER" in s_clean:
                continue
            if not s_clean.endswith(".JK"):
                s_clean = f"{s_clean}.JK"
            list_clean.append(s_clean)
            
        print(f"✅ Successfully loaded {len(list_clean)} stock tickers from column '{kolom_utama}'")
        return list_clean
    except Exception as e:
        print(f"❌ Failed to read CSV file: {e}")
        return ["BBRI.JK", "TLKM.JK", "ASII.JK"]

def jalankan_pemindaian():
    daftar_saham = muat_daftar_saham()
    if not daftar_saham:
        print("❌ No stocks available to process.")
        return
        
    print("🚀 Starting technical calculation process...")
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
            
            if bandwidth_sekarang <= 0.05 or bandwidth_sekarang == min_bandwidth_20h:
                volume_sekarang = df_analisis['Volume'].iloc[-1]
                rata_volume_20h = df_analisis['Volume'].tail(20).mean()
                
                status_vol = "Volume Mengering (Konsolidasi Berlanjut)"
                if volume_sekarang > (rata_volume_20h * 1.5):
                    status_vol = "🔥 VOLUME SPIKE! Bandar masuk, siap terbang!"
                
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
                
        except Exception as err:
            print(f"⚠️ Error reading ticker {kode_saham}: {err}")

if __name__ == "__main__":
    jalankan_pemindaian()
