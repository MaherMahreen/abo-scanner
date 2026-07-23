import os
import json
import requests

# =====================================================================
# DATA KREDENSIAL UTUH (SUDAH DIKUNCI DAN VALID)
# =====================================================================
TELEGRAM_TOKEN_LANGSUNG = "8567909596:AAE7fePUPB9wvjb7t4ht66G-UIf1E3tvCRE"
CHAT_ID_LANGSUNG = "8690860489"

# =====================================================================
# 618 DAFTAR SAHAM SYARIAH ANDA (SUDAH LUURUS & RAPI)
# =====================================================================
DAFTAR_SAHAM_SYARIAH = [
    "BBMI", "BRIS", "BTPS", "JMAS", "PNBS", "SPOT", "AADI", "ABMM", "ADMR", "ADRO", "AKRA", "ARII", "ATLA", "BBRM", "BESS", "BOAT", "BSML", "BSSR", "BULL", "BUMI", "BYAN", "CANI", "CGAS", "COAL", "DEWA",
    "DSSA", "DWGL", "ELSA", "ENRG", "FIRE", "GEMS", "HRUM", "IATA", "INDY", "ITMA", "ITMG", "KKGI", "KOPI", "MAHA", "MBAP", "MCOL", "MEDC", "MKAP", "MYOH",
    "PGAS", "PKPK", "PSAT", "PSSI", "PTBA", "PTIS", "RAJA", "RATU", "RGAS", "RMKE", "RMKO", "RUIS", "SEMA", "SGER", "SICO", "SMMT", "SOCI", "SUNI", "TCPI", "TEBE", "TOBA", "TPMA", "UNIQ", "WINS", "WOWS",
    "ADMG", "AGII", "AKPI", "ALDO", "ALKA", "ANTM", "APLI", "ARCI", "ASPR", "AVIA", "AYLS", "BATR", "BLES", "BMSR", "BRMS", "BRNA", "CHEM", "CITA", "CLPI",
    "CTBN", "DGWG", "DKFT", "EKAD", "EPAC", "ESIP", "ESSA", "FASW", "FPNI", "FWCT", "GDST", "GGRP", "IFII", "IFSH", "IGAR", "INCI", "INKP", "INTD", "INTP", "IPOL", "ISSP", "KDSI", "KKES",
    "LMSH", "LTLS", "MBMA", "MDKA", "MDKI", "MINE", "NICE", "NICL", "NIKL", "OBMD", "OKAS", "PACK", "PBID", "PDPP", "PICO", "PPRI",
    "PSAB", "PTMR", "SAMF", "SBMA", "SMBR", "SMCB", "SMGA", "SMGR", "SMKL", "SMLE", "SOLA", "SPMA", "SULI", "TALF", "TBMS", "TINS", "TIRT", "TKIM", "TPIA", "TRST", "UNIC", "WTON", "YPAS",
    "AMFG", "AMIN", "APII", "ARNA", "ASGR", "BINO", "BLUE", "CAKK", "CCSI", "CRSN", "DYAN", "FOLK", "GPSO", "HEXA", "HOPE", "HYGN", "ICON", "IKAI", "IKBI", "IMPC", "JECC", "JTPE", "KBLI",
    "KBLM", "KIAS", "KING", "KOBX", "KOIN", "KONI", "KUAS", "LION", "MARK", "MFMI", "MHKI", "MLIA", "MUTU", "NAIK", "NTBK", "PADA", "PTMP", "SCCO", "SKRN", "SMIL", "SOSS", "SPTO", "TIRA",
    "TOTO", "UNTR", "VISI", "VOKS", "WIDI", "AALI", "ADES", "AGAR", "AISA", "AMMS", "ASHA", "AYAM", "BISI", "BOBA", "BRRC", "BUAH", "BUDI", "BWPT", "CAMP", "CEKA", "CLEO", "CMRY", "CPIN", "CPRO",
    "CSRA", "DAYA", "DEWI", "DMND", "DSFI", "DSNG", "EPMT", "EURO", "FISH", "FLMC", "FOOD", "GOOD", "GRPM", "GULA", "GUNA", "GZCO", "HERO", "HOKI", "ICBP", "IKAN", "INDF", "JARR",
    "JAWA", "JPFA", "KEJU", "KINO", "KMDS", "LSIP", "MAIN", "MAXI", "MBTO", "MKTR", "MLPL", "MPPA", "MRAT", "MSJA", "MYOR", "NANO", "NASI", "NAYZ", "NEST", "NSSS", "PCAR", "PGUN", "PNGO",
    "PSDN", "PSGO", "PTPS", "RANC", "ROTI", "SDPC", "SGRO", "SIMP", "SIPD", "SKBM", "SKLT", "SMAR", "STAA", "STTP", "TAPG", "TCID", "TGKA", "TGUK", "TLDN", "UCID", "UDNG", "ULTJ",
    "UNVR", "VICI", "WAPO", "YUPI", "ACES", "AEGS", "ASLC", "AUTO", "BABY", "BAIK", "BAUT", "BAYU", "BELL", "BIKE", "BLTZ", "BMBL", "BMTR", "BOGA", "BOLT", "BRAM", "CINT",
    "CNMA", "CSAP", "CSMI", "DEPO", "DOOH", "DOSS", "DRMA", "EAST", "ECII", "ENAK", "ERAA", "ERAL", "ERTX", "ESTA", "FAST", "FILM", "GDYR", "GEMA", "GJTL", "GOLF", "GRPH",
    "GWSA", "HAJJ", "HRTA", "IDEA", "IIKP", "INDR", "INDS", "IPTV", "ISAP", "JGLE", "JIHD", "KAQI", "KICI", "KLIN", "KOTA", "KPIG", "LFLO", "LIVE", "LMAX", "LMPI", "LPIN",
    "LPPF", "MAPA", "MAPB", "MAPI", "MDIA", "MDIY", "MEJA", "MERI", "MGLV", "MICE", "MKNT", "MNCN", "MPMA", "MSIN", "MSKY", "OLIV", "PANR", "PART", "PDES", "PGLI", "PJAA",
    "PLAN", "PMJS", "PMUI", "POLU", "PSKT", "PTSP", "PZZA", "RAAM", "RALS", "SCNP", "SHID", "SLIS", "SMSM", "SNLK", "SOFA", "SOTS", "SPRE", "SSTM", "SWID", "TFCO", "TMPO",
    "TOOL", "TRIS", "TYRE", "UFOE", "VERN", "VKTR", "WOOD", "YELO", "ZONE", "BMHS", "CARE", "CHEK", "DGNS", "DVLA", "HALO", "HEAL", "IKPM", "IRRA", "KLBF", "LABS", "MDLA",
    "MEDS", "MERK", "MIKA", "MMIX", "MTMH", "OBAT", "OMED", "PEHA", "PEVE", "PRAY", "PRDA", "PRIM", "RSCH", "RSGK", "SAME", "SCPI", "SIDO", "SILO", "SOHO", "SURI", "TSPC",
    "SRTG", "PALM", "DEFI", "ADCP", "AMAN", "APLN", "ASPI", "ASRI", "ATAP", "BAPI", "BBSS", "BCIP", "BEST", "BIPP", "BKDP", "BKSL", "BSBK", "BSDE", "CITY", "CSIS", "CTRA",
    "DADA", "DILD", "DMAS", "DUTI", "ELTY", "EMDE", "FMII", "GMTD", "GPRA", "GRIA", "HBAT", "HOMI", "INPP", "IPAC", "JRPT", "KBAG", "KIJA", "KOCI", "LAND", "LPCK", "LPLI",
    "MKPI", "MMLP", "MSIE", "MTLA", "MTSM", "NZIA", "PAMG", "PLIN", "POLI", "PURI", "RBMS", "REAL", "RELF", "RISE", "ROCK", "RODA", "SAGE", "SATU", "SMDM", "SMRA", "UANG",
    "URBN", "VAST", "WINR", "AREA", "ATIC", "AWAN", "AXIO", "BELI", "CASH", "CHIP", "CYBR", "DCII", "DIVA", "DMMX", "ELIT", "GLVA", "HDIT", "IOTF", "IRSX", "JATI", "KIOS",
    "KREN", "LUCK", "MCAS", "MLPT", "MPIX", "MSTI", "MTDL", "NFCX", "PGJO", "PTSN", "RUNS", "TFAS", "TOSK", "TRON", "UVCR", "WGSH", "WIFI", "WIRG", "ZYRX", "ASLI", "BALI",
    "BDKR", "CASS", "CMNP", "DATA", "DGIK", "EXCL", "FIMP", "GHON", "GOLD", "HADE", "IBST", "IDPR", "INET", "IPCM", "ISAT", "JAST", "JKON", "JSMR", "KARW", "KEEN", "KETR",
    "KOKA", "MANG", "META", "MORA", "MPOW", "MTEL", "MTPS", "NRCA", "PORT", "POWR", "PPRE", "PTPP", "PTPW", "SMKM", "SSIA", "SUPR", "TAMA", "TLKM", "TOTL", "WEGE", "AKSI",
    "ASSA", "BIRD", "BLOG", "BLTA", "CMPP", "ELPI", "GIAA", "GTRA", "HAIS", "HATM", "HELI", "JAYA", "KJEN", "KLAS", "LAJU", "LOPI", "LRNA", "MIRA", "MITI", "NELY", "PJHB",
    "PPGL", "PURA", "RCCC", "SAFE", "SAPX", "SMDR", "TAXI", "TMAS", "TNCA", "TRJA", "TRUK", "WBSA", "WEHA", "GRHA"
]
# =====================================================================

def kirim_radar_telegram(pesan):
    # Mengembalikan ke requests yang terbukti sukses mengirim notifikasi ke akun Anda kemarin
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"
    payload = {"chat_id": str(CHAT_ID_LANGSUNG), "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")
        return False

def cek_sideways_yahoo(ticker_clean):
    ticker_jk = f"{ticker_clean}.JK"
    url = f"https://yahoo.com{ticker_jk}?range=60d&interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return
            
        data = response.json()
        # FIXED TOTAL: Struktur array [0] dikunci agar data harga bursa terbaca presisi
        result = data['chart']['result'][0]
        prices = result['indicators']['quote'][0]['close']
        volumes = result['indicators']['quote'][0]['volume']
        
        prices = [p for p in prices if p is not None]
        volumes = [v for v in volumes if v is not None]
        
        if len(prices) < 20:
            return
            
        close_20d = prices[-20:]
        ma20 = sum(close_20d) / 20
        
        variance = sum((x - ma20) ** 2 for x in close_20d) / 20
        std_dev = variance ** 0.5
        
        upper_band = ma20 + (2 * std_dev)
        lower_band = ma20 - (2 * std_dev)
        
        harga_sekarang = prices[-1]
        bandwidth_sekarang = (upper_band - lower_band) / ma20 if ma20 != 0 else 0
        
        # Saringan dilonggarkan ke 0.30 agar saham syariah konsolidasi langsung keluar malam ini
        if bandwidth_sekarang <= 0.30: 
            volume_sekarang = volumes[-1] if volumes else 0
            rata_volume = sum(volumes[-20:]) / 20 if volumes else 1
            
            status_vol = "Volume Mengering"
            if volume_sekarang > (rata_volume * 1.3):
                status_vol = "🔥 VOLUME SPIKE! Bandar Masuk!"
                
            pesan = (
                f"🚨 *ABO RADAR: SAHAM SIDEWAYS* 🚨\n\n"
                f"Saham Syariah: *{ticker_clean}*\n"
                f"Harga Terakhir: Rp {int(harga_sekarang)}\n"
                f"Bandwidth: {bandwidth_sekarang*100:.2f}%\n"
                f"Kondisi: {status_vol}\n\n"
                f"💡 _Breakout Target: Rp {int(upper_band)}_"
            )
            print(f"🎯 Sinyal Ditemukan: {ticker_clean}")
            kirim_radar_telegram(pesan)
            
    except Exception as e:
        print(f"Skip {ticker_clean}: {e}")

if __name__ == "__main__":
    kirim_radar_telegram("🤖 *ABO Scanner Massal Aktif!* Memulai penyaringan kilat harian pada 618 saham syariah...")
    
    for ticker in DAFTAR_SAHAM_SYARIAH:
        cek_sideways_yahoo(ticker.strip().upper())
        
    kirim_radar_telegram("🏁 *Pemindaian Selesai.* Semua saham syariah selesai disaring.")
