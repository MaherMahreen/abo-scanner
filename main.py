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
    Mengirimkan rekomendasi 5 saham terpilih dengan format HTML yang rapi.
    """
    if not bot_token or not chat_id:
        print("[ERROR] Kredensial Telegram kosong!")
        return

    if not stocks_analysis:
        msg = "<b>📊 Hasil ABO Scanner Massal</b>\n\n🎯 Hari ini tidak ditemukan emiten yang memenuhi kriteria sideways & breakout siap terbang."
    else:
        msg = "<b>📊 Hasil ABO Scanner Massal</b>\n"
        msg += "🎯 <i>Top 5 Emiten Sideways Lama & Siap Breakout (Terbang):</i>\n\n"
        for i, res in enumerate(stocks_analysis):
            msg += f"<b>{i+1}. {res['ticker']}</b>\n"
            msg += f"   • Kondisi: {res['status']}\n"
            msg += f"   • Range Sideways: Rp {res['low_bound']} - Rp {res['high_bound']}\n"
            msg += f"   • Harga Terakhir: Rp {res['close']}\n"
            msg += f"   • Lonjakan Volume: {res['vol_spike']:.1f}x lipat rata-rata\n\n"
    
    url = f"https://telegram.org{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.json().get("ok"):
            print("[OK] Notifikasi strategi breakout berhasil dikirim ke Telegram.")
        else:
            print(f"[X] Telegram menolak: {response.json().get('description')}")
    except Exception as e:
        print(f"[ERROR] Gagal mengirim notifikasi: {e}")


def hitung_analisis_breakout(ticker_symbol):
    """
    Menganalisis apakah sebuah saham sedang sideways lama dan menunjukkan tanda breakout volume.
    """
    try:
        # Mengunduh data historis
        ticker = yf.Ticker(f"{ticker_symbol}.JK")
        df = ticker.history(period="100d")
        
        if len(df) < 40:
            return None
            
        df['MA20_Vol'] = df['Volume'].rolling(window=20).mean()
        
        current_close = int(df['Close'].iloc[-1])
        current_volume = df['Volume'].iloc[-1]
        avg_volume_20d = df['MA20_Vol'].iloc[-1]
        
        hist_30d = df.iloc[-31:-1]
        highest_30d = hist_30d['High'].max()
        lowest_30d = hist_30d['Low'].min()
        
        price_channel_width = ((highest_30d - lowest_30d) / lowest_30d) * 100
        
        # Saringan Sideways & Breakout
        is_sideways = price_channel_width <= 12
        is_price_breakout = current_close >= (highest_30d * 0.99)
        vol_ratio = current_volume / avg_volume_20d if avg_volume_20d > 0 else 0
        is_volume_spike = vol_ratio >= 1.5
        
        if is_sideways and (is_price_breakout or is_volume_spike):
            status = "Breakout Konfirmasi Volume" if is_price_breakout and is_volume_spike else "Akumulasi Sideways Akhir"
            return {
                "ticker": ticker_symbol,
                "status": status,
                "low_bound": int(lowest_30d),
                "high_bound": int(highest_30d),
                "close": current_close,
                "vol_spike": vol_ratio
            }
    except Exception:
        pass
    return None


def run_scanner_logic():
    """
    Melakukan pemindaian massal terhadap daftar emiten untuk mencari 5 kandidat terbaik.
    """
    print("Memulai Score & Signal Engine: Pemindaian Sideways & Breakout...")
    
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
    
    kandidat_terpilih = []
    
    for code in raw_saham:
        analysis = hitung_analisis_breakout(code)
        if analysis:
            kandidat_terpilih.append(analysis)
            print(f"[FOUND] {code} cocok dengan kriteria.")
            
        time.sleep(0.2)
        
    kandidat_terpilih = sorted(kandidat_terpilih, key=lambda x: x['vol_spike'], reverse=True)
    top_5 = kandidat_terpilih[:5]
    return top_5

if __name__ == "__main__":
    saham_siap_terbang = run_scanner_logic()
    send_telegram_notification(TELEGRAM_TOKEN, CHAT_ID, saham_siap_terbang)
