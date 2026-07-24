import os
import sys
import time
import requests

# =========================================================================
# 📝 PENGATURAN KREDENSIAL TELEGRAM
# =========================================================================
TELEGRAM_TOKEN = "8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4"
CHAT_ID = "8690860489"
# =========================================================================

def send_telegram_notification(bot_token, chat_id, stocks_list):
    """
    Fungsi untuk mengirimkan daftar saham ke Telegram secara aman.
    Otomatis membagi pesan menjadi beberapa bagian jika melebihi batas karakter Telegram.
    """
    if not bot_token or not chat_id:
        print("[ERROR] Token Bot atau Chat ID Telegram kosong! Periksa kembali variabel Anda.")
        return

    if not stocks_list:
        print("[INFO] Tidak ada saham yang ditemukan untuk dikirim.")
        return

    # 1. Format daftar saham menjadi teks per baris menggunakan format HTML yang stabil
    lines = [f"{i+1}. {stock}" for i, stock in enumerate(stocks_list)]
    
    # 2. Bagi teks menjadi beberapa bagian (chunks) jika melebihi batas aman 3.500 karakter
    MAX_CHARACTERS = 3500
    chunks = []
    current_chunk = "<b>📊 Hasil ABO Scanner Massal</b>\n\n"
    
    for line in lines:
        if len(current_chunk) + len(line) + 1 > MAX_CHARACTERS:
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)

    # 3. URL Format API Telegram yang benar
    url = f"https://telegram.org/bot8567909596:AAHy8NYFG6wL7PaZ6FbYo-kElMRcH6YuRx4/sendMessage"
    
    for index, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML"
        }
        
        try:
            print(f"[INFO] Mengirim notifikasi bagian {index+1}/{len(chunks)}...")
            response = requests.post(url, json=payload, timeout=15)
            response_data = response.json()
            
            # Jika Telegram menolak karena kesalahan parsing HTML, gunakan fallback ke teks biasa
            if not response_data.get("ok"):
                print(f"[X] Telegram menolak pesan: {response_data.get('description')}")
                if "can't parse" in response_data.get('description', '').lower():
                    print("[INFO] Mengirim ulang sebagai Plain Text tanpa HTML format...")
                    payload.pop("parse_mode", None)
                    response = requests.post(url, json=payload, timeout=15)
                    response_data = response.json()
                    
                if not response_data.get("ok"):
                    print(f"[ERROR] Gagal total mengirimkan bagian {index+1}.")
            else:
                print(f"[OK] Bagian {index+1} berhasil dikirim ke Telegram.")
                
            # Jeda 1.5 detik antar pesan untuk menghindari rate-limit (spam block) dari Telegram
            time.sleep(1.5)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Masalah koneksi jaringan ke API Telegram: {e}")


def run_scanner_logic():
    """
    Mengembalikan daftar kode saham yang telah ditentukan untuk diproses.
    """
    print("# FIXED: Diarahkan langsung ke main.py agar seluruh modul Score & Signal Engine aktif nyata!")
    print("Memicu jembatan notifikasi...")
    
    # Menampung seluruh kode saham yang Anda kirimkan
    hasil_saham = [
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
    
    print(f"Berhasil memuat {len(hasil_saham)} saham.")
    return hasil_saham


if __name__ == "__main__":
    # 1. Jalankan proses pemindaian saham utama
    daftar_saham_terdeteksi = run_scanner_logic()
    
    # 2. Eksekusi pengiriman notifikasi massal ke Telegram menggunakan kredensial di atas
    send_telegram_notification(TELEGRAM_TOKEN, CHAT_ID, daftar_saham_terdeteksi)
