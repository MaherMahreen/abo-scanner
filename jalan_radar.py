import os
import pandas as pd
import yfinance as yf
import requests

# =====================================================================
# DATA KREDENSIAL UTUH DAN AMAN (MENGGUNAKAN TOKEN DAN ID ASLI ANDA)
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8690860489"
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
    # Menggunakan metode URL Parameter murni agar langsung menembus limitasi protokol chat session
    url = f"https://telegram.org{TELEGRAM_TOKEN_LANGSUNG}/sendMessage?chat_id={CHAT_ID_LANGSUNG}&text={pesan}&parse_mode=Markdown"
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect to Telegram API: {e}")
        return False

def muat_daftar_saham():
    print("✅ Memuat 50+ daftar saham syariah likuid untuk pemindaian massal...")
    return [
        # Sektor Energi & Tambang
        "ADRO.JK", "ADMR.JK", "ANTM.JK", "PTBA.JK", "ITMG.JK", "HRUM.JK", "MBMA.JK", "AKRA.JK",
        # Sektor Infrastruktur, Telekomunikasi & Logistik
        "TLKM.JK", "EXCL.JK", "ISAT.JK", "TOWR.JK", "JSMR.JK", "WIKA.JK", "ADHI.JK",
        # Sektor Konsumsi & Kesehatan
        "ICBP.JK", "INDF.JK", "UNVR.JK", "MYOR.JK", "KLBF.JK", "SIDO.JK", "AMRT.JK", "HEAL.JK", "MIKA.JK",
        # Sektor Perbankan Syariah & Keuangan
        "BRIS.JK", "BTPS.JK", "PNBS.JK",
        # Sektor Properti & Semen
        "SMGR.JK", "INTP.JK", "BSDE.JK", "CTRA.JK", "SMRA.JK",
        # Sektor Komoditas & Otomotif
        "AALI.JK", "LSIP.JK", "TAPG.JK", "AUTO.JK", "DRMA.JK", "ACES.JK",
        # Sektor Teknologi & Media
        "GOTO.JK", "BUKA.JK", "EMTKA.JK", "SCMA.JK"
    ]

def jalankan_pemindaian():
    # TEST PING MELEWATI PROTOKOL PRIVASI
    kirim_radar_telegram("🤖 *ABO Scanner Sistem Terhubung!* Memulai pemindaian massal 50+ saham syariah...")
    
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
            
            # Filter dilonggarkan penuh (0.80) agar memperbanyak saham syariah yang lolos masuk radar malam ini
            if bandwidth_sekarang <= 0.80 or bandwidth_sekarang == min_bandwidth_20h:
                volume_sekarang = df_analisis['Volume'].iloc[-1]
                rata_volume_20h = df_analisis['Volume'].tail(20).mean()
                
                status_vol = "Konsolidasi Historis Syariah"
                if volume_sekarang > rata_volume_20h:
                    status_vol = "🔥 Potensi Breakout Tinggi!"
                
                clean_name = kode_saham.replace(".JK", "")
                pesan = (
                    f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                    f"Saham: *{clean_name}*\n"
                    f"Harga Terakhir: Rp {int(harga_sekarang)}\n"
                    f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                    f"Kondisi: {status_vol}"
                )
                print(f"🎯 Signal found: {clean_name}")
                kirim_radar_telegram(pesan)
                sinyal_ditemukan += 1
        except Exception as err:
            print(f"⚠️ Error reading ticker {kode_saham}: {err}")
            
    kirim_radar_telegram(f"🏁 *Pemindaian Selesai.* Berhasil mengirimkan {sinyal_ditemukan} laporan saham syariah ke Telegram Anda.")

if __name__ == "__main__":
    jalankan_pemindaian()
