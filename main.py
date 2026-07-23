import os
import pandas as pd
import yfinance as yf
from indikator import hitung_bollinger_squeeze
from telegram import kirim_radar_telegram

def muat_daftar_saham():
    nama_file = "saham_syariah.csv"
    if not os.path.exists(nama_file):
        print(f"⚠️ Peringatan: File {nama_file} tidak ditemukan! Menggunakan daftar cadangan.")
        return ["BBRI.JK", "TLKM.JK", "ASII.JK"]
        
    try:
        df_saham = pd.read_csv(nama_file)
        
        # DEBUG: Cetak daftar kolom yang terbaca agar terlihat jika ada typo/salah nama kolom
        print(f"📊 Kolom yang terdeteksi di CSV Anda: {list(df_saham.columns)}")
        
        # Otomatis mengambil kolom pertama apa pun namanya
        kolom_utama = df_saham.columns[0]
        list_saham = df_saham[kolom_utama].dropna().astype(str).tolist()
        
        list_clean = []
        for s in list_saham:
            s_clean = s.strip().upper()
            # Hapus imbuhan pembatas atau spasial jika tidak sengaja terbaca
            if s_clean == "" or "KODE" in s_clean or "TICKER" in s_clean:
                continue
            if not s_clean.endswith(".JK"):
                s_clean = f"{s_clean}.JK"
            list_clean.append(s_clean)
            
        print(f"✅ Berhasil memuat {len(list_clean)} kode saham dari kolom '{kolom_utama}'")
        return list_clean
    except Exception as e:
        print(f"❌ Gagal membaca file CSV: {e}")
        return ["BBRI.JK", "TLKM.JK", "ASII.JK"]

def jalankan_pemindaian():
    daftar_saham = muat_daftar_saham()
    if not daftar_saham:
        print("❌ Tidak ada saham yang bisa diproses.")
        return
        
    print("🚀 Memulai proses kalkulasi teknikal...")
    for kode_saham in daftar_saham:
        try:
            ticker = yf.Ticker(kode_saham)
            # Batasi pengambilan data awal agar tidak terkena limit pembatasan akses Yahoo
            data_historis = ticker.history(period="60d")
            
            if data_historis.empty or len(data_historis) < 20:
                # Lewati senyap jika ticker kosong/tidak valid di Yahoo Finance
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
                
                print(f"🎯 Sinyal ditemukan: {clean_name}")
                kirim_radar_telegram(pesan)
                
        except Exception as err:
            print(f"⚠️ Kendala membaca data saham {kode_saham}: {err}")

if __name__ == "__main__":
    jalankan_pemindaian()
