import os
import sys
import time
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# =========================================================================
# PENGATURAN KREDENSIAL TELEGRAM (SUDAH VALID)
# =========================================================================
TELEGRAM_TOKEN = "8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc"
CHAT_ID = "8690860489"
# =========================================================================

def send_telegram_notification(bot_token, chat_id, text_msg):
    """
    Fungsi pengirim pesan Telegram standar aman.
    Menggunakan URL wajib api.telegram.org/bot dan pengecekan status respons riil.
    """
    url = f"https://api.telegram.org/bot8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc/sendMessage"
    payload = {"chat_id": chat_id, "text": text_msg, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        print("[STATUS]", response.status_code)
        print(response.text)

        if response.status_code == 200:
            print("[OK] Telegram berhasil mengirimkan sinyal PRO.")
        else:
            print("[ERROR] Telegram gagal.")
    except Exception as e:
        print("[ERROR] Gagal kirim Telegram:", e)

def run_scanner_logic():
    print("Memulai ULTIMATE PRO Bulk Download Engine...")
    raw_saham = [
        "BBMI", "BRIS", "BTPS", "JMAS", "PNBS", "SPOT", "AADI", "ABMM", "ADMR", "ADRO", 
        "AKRA", "ARII", "ATLA", "BBRM", "BESS", "BOAT", "BSML", "BSSR", "BULL", "BUMI", 
        "BYAN", "CANI", "CGAS", "COAL", "DEWA", "DSSA", "DWGL", "ELSA", "ENRG", "FIRE", 
        "GEMS", "HRUM", "IATA", "INDY", "ITMA", "ITMG", "KKGI", "KOPI", "MAHA", "MBAP", 
        "MCOL", "MEDC", "MKAP", "MYOH", "PGAS", "PKPK", "PSAT", "PSSI", "PTBA", "PTIS", 
        "RAJA", "RATU", "RGAS", "RMKE", "RMKO", "RUIS", "SEMA", "SGER", "SICO", "SMMT", 
        "SOCI", "SUNI", "TCPI", "TEBE", "TOBA", "TPMA", "UNIQ", "WINS", "WOWS", "ADMG", 
        "AGII", "AKPI", "ALDO", "ALKA", "ANTM", "APLI", "ARCI", "ASPR", "AVIA", "AYLS", 
        "BATR", "BLES", "BMSR", "BRMS", "BRNA", "CHEM", "CITA", "CLPI", "CTBN", "DGWG", 
        "DKFT", "EKAD", "EPAC", "ESIP", "ESSA", "FASW", "FPNI", "FWCT", "GDST", "GGRP", 
        "IFII", "IFSH", "IGAR", "INCI", "INKP", "INTD", "INTP", "IPOL", "ISSP", "KDSI", 
        "KKES", "LMSH", "LTLS", "MBMA", "MDKA", "MDKI", "MINE", "NICE", "NICL", "NIKL", 
        "OBMD", "OKAS", "PACK", "PBID", "PDPP", "PICO", "PPRI", "PSAB", "PTMR", "SAMF", 
        "SBMA", "SMBR", "SMCB", "SMGA", "SMGR", "SMKL", "SMLE", "SOLA", "SPMA", "SULI", 
        "TALF", "TBMS", "TINS", "TIRT", "TKIM", "TPIA", "TRST", "UNIC", "WTON", "YPAS", 
        "AMFG", "AMIN", "APII", "ARNA", "ASGR", "BINO", "BLUE", "CAKK", "CCSI", "CRSN", 
        "DYAN", "FOLK", "GPSO", "HEXA", "HOPE", "HYGN", "ICON", "IKAI", "IKBI", "IMPC", 
        "JECC", "JTPE", "KBLI", "KBLM", "KIAS", "KING", "KOBX", "KOIN", "KONI", "KUAS", 
        "LION", "MARK", "MFMI", "MHKI", "MLIA", "MUTU", "NAIK", "NTBK", "PADA", "PTMP", 
        "SCCO", "SKRN", "SMIL", "SOSS", "SPTO", "TIRA", "TOTO", "UNTR", "VISI", "VOKS", 
        "WIDI", "AALI", "ADES", "AGAR", "AISA", "AMMS", "ASHA", "AYAM", "BISI", "BOBA", 
        "BRRC", "BUAH", "BUDI", "BWPT", "CAMP", "CEKA", "CLEO", "CMRY", "CPIN", "CPRO"
    ]
    raw_saham_ext = [
        "CSRA", "DAYA", "DEWI", "DMND", "DSFI", "DSNG", "EPMT", "EURO", "FISH", "FLMC", 
        "FOOD", "GOOD", "GRPM", "GULA", "GUNA", "GZCO", "HERO", "HOKI", "ICBP", "IKAN", 
        "INDF", "JARR", "JAWA", "JPFA", "KEJU", "KINO", "KMDS", "LSIP", "MAIN", "MAXI", 
        "MBTO", "MKTR", "MLPL", "MPPA", "MRAT", "MSJA", "MYOR", "NANO", "NASI", "NAYZ", 
        "NEST", "NSSS", "PCAR", "PGUN", "PNGO", "PSDN", "PSGO", "PTPS", "RANC", "ROTI", 
        "SDPC", "SGRO", "SIMP", "SIPD", "SKBM", "SKLT", "SMAR", "STAA", "STTP", "TAPG", 
        "TCID", "TGKA", "TGUK", "TLDN", "UCID", "UDNG", "ULTJ", "UNVR", "VICI", "WAPO", 
        "YUPI", "ACES", "AEGS", "ASLC", "AUTO", "BABY", "BAIK", "BAUT", "BAYU", "BELL", 
        "BIKE", "BLTZ", "BMBL", "BMTR", "BOGA", "BOLT", "BRAM", "CINT", "CNMA", "CSAP", 
        "CSMI", "DEPO", "DOOH", "DOSS", "DRMA", "EAST", "ECII", "ENAK", "ERAA", "ERAL", 
        "ERTX", "ESTA", "FAST", "FILM", "GDYR", "GEMA", "GJTL", "GOLF", "GRPH", "GWSA", 
        "HAJJ", "HRTA", "IDEA", "IIKP", "INDR", "INDS", "IPTV", "ISAP", "JGLE", "JIHD", 
        "KAQI", "KICI", "KLIN", "KOTA", "KPIG", "LFLO", "LIVE", "LMAX", "LMPI", "LPIN", 
        "LPPF", "MAPA", "MAPB", "MAPI", "MDIA", "MDIY", "MEJA", "MERI", "MGLV", "MICE", 
        "MKNT", "MNCN", "MPMA", "MSIN", "MSKY", "OLIV", "PANR", "PART", "PDES", "PGLI", 
        "PJAA", "PLAN", "PMJS", "PMUI", "POLU", "PSKT", "PTSP", "PZZA", "RAAM", "RALS", 
        "SCNP", "SHID", "SLIS", "SMSM", "SNLK", "SOFA", "SOTS", "SPRE", "SSTM", "SWID", 
        "TFCO", "TMPO", "TOOL", "TRIS", "TYRE", "UFOE", "VERN", "VKTR", "WOOD", "YELO", 
        "ZONE", "BMHS", "CARE", "CHEK", "DGNS", "DVLA", "HALO", "HEAL", "IKPM", "IRRA", 
        "KLBF", "LABS", "MDLA", "MEDS", "MERK", "MIKA", "MMIX", "MTMH", "OBAT", "OMED", 
        "PEHA", "PEVE", "PRAY", "PRDA", "PRIM", "RSCH", "RSGK", "SAME", "SCPI", "SIDO", 
        "SILO", "SOHO", "SURI", "TSPC", "SRTG", "PALM", "DEFI", "ADCP", "AMAN", "APLN", 
        "ASPI", "ASRI", "ATAP", "BAPI", "BBSS", "BCIP", "BEST", "BIPP", "BKDP", "BKSL", 
        "BSBK", "BSDE", "CITY", "CSIS", "CTRA", "DADA", "DILD", "DMAS", "DUTI", "ELTY", 
        "EMDE", "FMII", "GMTD", "GPRA", "GRIA", "HBAT", "HOMI", "INPP", "IPAC", "JRPT", 
        "KBAG", "KIJA", "KOCI", "LAND", "LPCK", "LPLI", "MKPI", "MMLP", "MSIE", "MTLA", 
        "MTSM", "NZIA", "PAMG", "PLIN", "POLI", "PURI", "RBMS", "REAL", "RELF", "RISE", 
        "ROCK", "RODA", "SAGE", "SATU", "SMDM", "SMRA", "UANG", "URBN", "VAST", "WINR", 
        "AREA", "ATIC", "AWAN", "AXIO", "BELI", "CASH", "CHIP", "CYBR", "DCII", "DIVA", 
        "DMMX", "ELIT", "GLVA", "HDIT", "IOTF", "IRSX", "JATI", "KIOS", "KREN", "LUCK", 
        "MCAS", "MLPT", "MPIX", "MSTI", "MTDL", "NFCX", "PGJO", "PTSN", "RUNS", "TFAS", 
        "TOSK", "TRON", "UVCR", "WGSH", "WIFI", "WIRG", "ZYRX", "ASLI", "BALI", "BDKR", 
        "CASS", "CMNP", "DATA", "DGIK", "EXCL", "FIMP", "GHON", "GOLD", "HADE", "IBST", 
        "IDPR", "INET", "IPCM", "ISAT", "JAST", "JKON", "JSMR", "KARW", "KEEN", "KETR", 
        "KOKA", "MANG", "META", "MORA", "MPOW", "MTEL", "MTPS", "NRCA", "PORT", "POWR", 
        "PPRE", "PTPP", "PTPW", "SMKM", "SSIA", "SUPR", "TAMA", "TLKM", "TOTL", "WEGE", 
        "AKSI", "ASSA", "BIRD", "BLOG", "BLTA", "CMPP", "ELPI", "GIAA", "GTRA", "HAIS", 
        "HATM", "HELI", "JAYA", "KJEN", "KLAS", "LAJU", "LOPI", "LRNA", "MIRA", "MITI", 
        "NELY", "PJHB", "PPGL", "PURA", "RCCC", "SAFE", "SAPX", "SMDR", "TAXI", "TMAS", 
        "TNCA", "TRJA", "TRUK", "WBSA", "WEHA", "GRHA"
    ]
    raw_saham.extend(raw_saham_ext)
    tickers_jk = [f"{ticker}.JK" for ticker in raw_saham]
    kandidat_terpilih = []
    backup_saham = []
    
    try:
        raw_data = yf.download(
            tickers_jk,
            period="100d",
            group_by="ticker",
            auto_adjust=False,
            progress=False,
            threads=True
        )
    except Exception as e:
        print("[ERROR] Masalah unduhan Yahoo Finance:", e)
        return "<b>Hasil ABO Scanner Massal</b>\n\nGagal memuat data bursa."
    for ticker in raw_saham:
        try:
            symbol = f"{ticker}.JK"
            if not isinstance(raw_data.columns, pd.MultiIndex):
                continue
            if symbol not in raw_data.columns.get_level_values(0):
                continue
                
            df_ticker = raw_data[symbol].dropna().copy()
            if len(df_ticker) < 50:
                continue
                
            df_ticker['EMA20'] = df_ticker['Close'].ewm(span=20, adjust=False).mean()
            df_ticker['EMA50'] = df_ticker['Close'].ewm(span=50, adjust=False).mean()
            
            ma20_vol = df_ticker['Volume'].rolling(window=20).mean().iloc[-1]
            current_close = df_ticker['Close'].iloc[-1]
            current_volume = df_ticker['Volume'].iloc[-1]
            current_high = df_ticker['High'].iloc[-1]
            current_low = df_ticker['Low'].iloc[-1]
            
            c_ema20 = df_ticker['EMA20'].iloc[-1]
            c_ema50 = df_ticker['EMA50'].iloc[-1]
            
            if ma20_vol > 0 and not pd.isna(current_close):
                backup_saham.append({"ticker": ticker, "close": int(current_close), "ma_vol": ma20_vol})
            
            hist_20d = df_ticker.iloc[-21:-1]
            highest_20d = hist_20d['High'].max()
            lowest_20d = hist_20d['Low'].min()
            
            if lowest_20d == 0 or pd.isna(lowest_20d):
                continue
                
            price_channel_width = ((highest_20d - lowest_20d) / lowest_20d) * 100
            is_sideways = price_channel_width <= 22.0
            is_price_breakout = current_close >= (highest_20d * 0.96)
            vol_ratio = current_volume / ma20_vol if ma20_vol > 0 else 0
            is_volume_moving = vol_ratio >= 1.0
            
            if is_sideways and (is_price_breakout or is_volume_moving):
                is_uptrend = current_close >= c_ema20 and c_ema20 >= c_ema50
                
                range_harian = current_high - current_low
                posisi_tutup = current_close - current_low
                is_bullish_vsa = posisi_tutup >= (range_harian * 0.5) if range_harian > 0 else True
                
                status = "Strong Breakout + Akumulasi" if is_price_breakout and is_bullish_vsa else "Konsolidasi Bullish Sideways"
                if not is_uptrend:
                    status += " (Fase Bottoming)"
                
                stop_loss = int(lowest_20d * 0.98)
                target_profit = int(current_close + ((current_close - stop_loss) * 2))
                
                # REKOMENDASI 4: Hitung Rasio Risk to Reward (R:R) Riil Berbasis Selisih Papan Harga
                risk = current_close - stop_loss
                reward = target_profit - current_close
                rr = reward / risk if risk > 0 else 0
                
                # REKOMENDASI 3: Penggabungan Bobot Penilaian Multi-Faktor (Maksimal Skor 10)
                score_weight = 4.0 if is_price_breakout else 2.0
                score_weight += 3.0 if is_uptrend else 1.0
                score_weight += 3.0 if vol_ratio >= 2.0 else (vol_ratio * 1.5)
                final_score = min(round(score_weight, 1), 10.0)
                
                kandidat_terpilih.append({
                    "ticker": ticker,
                    "status": status,
                    "close": int(current_close),
                    "vol_spike": vol_ratio,
                    "sl": stop_loss,
                    "tp": target_profit,
                    "trend": "Bullish" if is_uptrend else "Sideways",
                    "rr": rr,
                    "score": final_score
                })
        except Exception as e:
            print(f"[ERROR EMITEN] {ticker}: {type(e).__name__} - {e}")
    # MENYUSUN NOTIFIKASI TELEGRAM FORMAT PRO UTUH DENGAN FOOTER & TIMESTAMP
    msg = "<b>🚀 SIAP TO THE MOON - PRO SCANNER</b>\n\n"
    if kandidat_terpilih:
        # REKOMENDASI 2: Tampilkan Informasi Total Jumlah Kandidat yang Berhasil Lolos Saringan
        msg += f"📊 Total Kandidat Berhasil Lolos: <b>{len(kandidat_terpilih)}</b>\n\n"
        msg += "🎯 <i>Top 5 Emiten Rekomendasi Terkuat (Urutan Berdasarkan Score Terpadu):</i>\n\n"
        
        # Pengurutan Pro: Diurutkan berdasarkan gabungan Skor Terpadu, bukan hanya Vol Spike saja
        kandidat_terpilih = sorted(kandidat_terpilih, key=lambda x: (x['score'], x['vol_spike']), reverse=True)
        for i, res in enumerate(kandidat_terpilih[:5]):
            msg += f"<b>{i+1}. {res['ticker']} (Rp {res['close']})</b>\n"
            msg += f"   • Sinyal: {res['status']}\n"
            msg += f"   • Trend: {res['trend']}\n"
            msg += f"   • Volume: {res['vol_spike']:.1f}x Vol Spike\n"
            msg += f"   • ⭐ <b>Score</b>: {res['score']}/10\n"
            msg += f"   • ⚖️ <b>R:R</b>: {res['rr']:.1f} : 1\n"
            msg += f"   • Buy: Sekarang (Area Market)\n"
            msg += f"   • TP: Rp {res['tp']}\n"
            msg += f"   • SL: Rp {res['sl']}\n\n"
    else:
        msg += "📈 <i>Kondisi bursa tenang / libur. Berikut Top 5 Saham Akumulasi Volume Terbesar Pasar:</i>\n\n"
        backup_saham = sorted(backup_saham, key=lambda x: x['ma_vol'], reverse=True)
        for i, res in enumerate(backup_saham[:5]):
            msg += f"<b>{i+1}. {res['ticker']} (Rp {res['close']})</b>\n"
            msg += f"   • Status: Akumulasi Volume Tinggi\n"
            msg += f"   • Rata-rata Vol 20 Hari: {res['ma_vol']:,.0f}\n"
            msg += f"   • 🎯 Target Resisten Terdekat: Rp {int(res['close']*1.07)}\n\n"
            
    # REKOMENDASI 5 & 1: Penambahan Pembatas Footer Sistem dan Jejak Waktu Eksplisit Scan WIB
    msg += "━━━━━━━━━━━━━━\n"
    msg += "🤖 ABO Scanner PRO\n"
    msg += "📡 Data: Yahoo Finance\n"
    msg += f"🕒 Scan: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    return msg

if __name__ == "__main__":
    teks_notifikasi = run_scanner_logic()
    send_telegram_notification(TELEGRAM_TOKEN, CHAT_ID, teks_notifikasi)
