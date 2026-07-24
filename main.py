import os
import sys
import time
import requests
import yfinance as yf
import pandas as pd
import numpy as np

# =========================================================================
# 📝 PENGATURAN KREDENSIAL TELEGRAM
# =========================================================================
TELEGRAM_TOKEN = "8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc"
CHAT_ID = "8690860489"
# =========================================================================

def send_telegram_notification(bot_token, chat_id, stocks_analysis):
    """
    Mengirimkan rekomendasi saham terpilih dengan format HTML yang rapi ke Telegram.
    """
    if not bot_token or not chat_id:
        print("[ERROR] Kredensial Telegram kosong!")
        return

    if not stocks_analysis:
        msg = "<b>📊 Hasil ABO Scanner Massal</b>\n\n🎯 Hari ini tidak ditemukan emiten yang memenuhi kriteria sideways & breakout siap terbang."
    else:
        msg = "<b>📊 Hasil ABO Scanner Massal</b>\n"
        msg += f"🎯 <i>Ditemukan {len(stocks_analysis)} emiten potensial. Ini Top 5 Terkuat:</i>\n\n"
        for i, res in enumerate(stocks_analysis[:5]):
            msg += f"<b>{i+1}. {res['ticker']}</b>\n"
            msg += f"   • Kondisi: {res['status']}\n"
            msg += f"   • Range Sideways: Rp {res['low_bound']} - Rp {res['high_bound']}\n"
            msg += f"   • Harga Terakhir: Rp {res['close']}\n"
            msg += f"   • Lonjakan Volume: {res['vol_spike']:.1f}x rata-rata\n\n"
    
    url = f"https://telegram.org/bot8567909596:AAFwit3UXmDVY7dn2qPjectOpN_1ywYeybc/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.json().get("ok"):
            print("[OK] Notifikasi strategi breakout berhasil dikirim ke Telegram.")
        else:
            print(f"[X] Telegram menolak: {response.json().get('description')}")
    except Exception as e:
        print(f"[ERROR] Gagal mengirim notifikasi: {e}")

def run_scanner_logic():
    print("Memulai Bulk Download Engine dengan Normalisasi Tabel Bertingkat...")
    
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
        "BRRC", "BUAH", "BUDI", "BWPT", "CAMP", "CEKA", "CLEO", "CMRY", "CPIN", "CPRO", 
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
    
    tickers_jk = [f"{ticker}.JK" for ticker in raw_saham]
    
    try:
        # Ambil data pasar historis secara sekaligus
        raw_data = yf.download(tickers_jk, period="60d", progress=False)
        
        # OBLIGATORI: Meluruskan tabel kolom bertingkat (Multi-Index) yfinance agar bisa dibaca normal
        raw_data.columns = ['_'.join(col).strip() for col in raw_data.columns.values]
    except Exception as e:
        print(f"[ERROR] Masalah unduhan Yahoo Finance: {e}")
        return []

    kandidat_terpilih = []
    
    for ticker in raw_saham:
        try:
            # Ambil kolom yang tepat berdasarkan nama kombinasi hasil pelurusan tabel
            close_col = f"Close_{ticker}.JK"
            high_col = f"High_{ticker}.JK"
            low_col = f"Low_{ticker}.JK"
            vol_col = f"Volume_{ticker}.JK"
            
            # Validasi ketersediaan data di dalam hasil unduhan bulk
            if close_col not in raw_data.columns:
                continue
                
            # Bersihkan baris data kosong dari emiten terkait
            df_ticker = raw_data[[close_col, high_col, low_col, vol_col]].dropna()
            
            if len(df_ticker) < 20:
                continue
                
            # Hitung Moving Average Volume 20 hari
            ma20_vol = df_ticker[vol_col].rolling(window=20).mean().iloc[-1]
            
            current_close = df_ticker[close_col].iloc[-1]
            current_volume = df_ticker[vol_col].iloc[-1]
            
            # Data historis 20 hari ke belakang sebelum hari ini untuk mengukur rentang Sideways
            hist_20d = df_ticker.iloc[-21:-1]
            highest_20d = hist_20d[high_col].max()
            lowest_20d = hist_20d[low_col].min()
            
            if lowest_20d == 0 or pd.isna(lowest_20d):
                continue
                
            # Saringan Longgar: Mengukur lebar ruang konsolidasi sideways dalam % (Batas aman: 20%)
            price_channel_width = ((highest_20d - lowest_20d) / lowest_20d) * 100
            is_sideways = price_channel_width <= 20.0
            
            # Saringan Pemicu Terbang: Mengukur apakah harga mendekati atau menembus batas atas
            is_price_breakout = current_close >= (highest_20d * 0.97)
            
