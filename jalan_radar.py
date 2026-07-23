# ============================================================
# ABO SCANNER RADAR v2.0
# Requests + Yahoo Finance API
# GitHub Actions Ready
# ============================================================

import os
import time
import requests
import pandas as pd

# ============================================================
# TELEGRAM
# ============================================================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKENNYA_NANTI_SAYA_ISI")
CHAT_ID = os.getenv("CHAT_ID", "8690860489")

# ============================================================
# YAHOO FINANCE
# ============================================================

BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 20
RETRY = 3

# ============================================================
# TELEGRAM SENDER
# ============================================================

def kirim_telegram(pesan):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown"
    }

    for i in range(RETRY):

        try:

            r = requests.post(
                url,
                data=payload,
                timeout=REQUEST_TIMEOUT
            )

            if r.status_code == 200:
                print("Telegram OK")
                return True

            print(
                f"Telegram Error "
                f"{r.status_code} : {r.text}"
            )

        except Exception as e:

            print(
                f"Telegram Retry {i+1} : {e}"
            )

        time.sleep(2)
# ============================================================
# AMBIL DATA YAHOO FINANCE
# ============================================================

def ambil_data_yahoo(kode):

    symbol = f"{kode}.JK"

    url = (
        f"{BASE_URL}/{symbol}"
        "?range=3mo"
        "&interval=1d"
    )

    for percobaan in range(RETRY):

        try:

            r = requests.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            if r.status_code != 200:

                print(
                    f"{kode} gagal HTTP {r.status_code}"
                )

                time.sleep(1)

                continue

            data = r.json()

            chart = data.get("chart", {})

            result = chart.get("result")

            if not result:

                print(f"{kode} tidak memiliki data.")

                return None

            quote = result[0]["indicators"]["quote"][0]

            close = quote.get("close", [])
            volume = quote.get("volume", [])

            # buang nilai None
            harga = []
            vol = []

            for h, v in zip(close, volume):

                if h is None:
                    continue

                harga.append(float(h))

                if v is None:
                    vol.append(0)
                else:
                    vol.append(float(v))

            if len(harga) < 30:

                print(
                    f"{kode} data kurang dari 30 hari."
                )

                return None

            return {

                "kode": kode,

                "close": harga,

                "volume": vol

            }

        except Exception as e:

            print(
                f"{kode} retry "
                f"{percobaan+1} : {e}"
            )

            time.sleep(2)

    return None
    # ============================================================
# PERHITUNGAN BOLLINGER BAND
# ============================================================

def hitung_bollinger(close, periode=20):

    if len(close) < periode:
        return None

    data = close[-periode:]

    ma = sum(data) / periode

    variance = sum((x - ma) ** 2 for x in data) / periode

    std = variance ** 0.5

    upper = ma + (2 * std)

    lower = ma - (2 * std)

    bandwidth = 0

    if ma != 0:
        bandwidth = (upper - lower) / ma

    return {

        "ma20": ma,

        "upper": upper,

        "lower": lower,

        "std": std,

        "bandwidth": bandwidth

    }


# ============================================================
# CEK VOLUME
# ============================================================

def analisa_volume(volume):

    if len(volume) < 20:

        return {

            "rata": 0,

            "sekarang": 0,

            "status": "Tidak Ada Data"

        }

    rata = sum(volume[-20:]) / 20

    sekarang = volume[-1]

    status = "Normal"

    if sekarang < rata * 0.70:

        status = "Volume Mengering"

    elif sekarang > rata * 1.50:

        status = "Volume Spike"

    return {

        "rata": rata,

        "sekarang": sekarang,

        "status": status

    }

    # ============================================================
# DETEKSI SIDEWAYS
# ============================================================

BANDWIDTH_SIDEWAYS = 0.35      # 35%
BREAKOUT_BUFFER = 0.01         # 1%

def cek_sideways(data):

    if data is None:
        return None

    close = data["close"]
    volume = data["volume"]

    bb = hitung_bollinger(close)

    if bb is None:
        return None

    vol = analisa_volume(volume)

    harga = close[-1]

    bandwidth = bb["bandwidth"]

    target_breakout = bb["upper"] * (1 + BREAKOUT_BUFFER)

    sideways = bandwidth <= BANDWIDTH_SIDEWAYS

    return {

        "kode": data["kode"],

        "harga": harga,

        "bandwidth": bandwidth,

        "upper": bb["upper"],

        "lower": bb["lower"],

        "ma20": bb["ma20"],

        "target": target_breakout,

        "volume": vol["status"],

        "sideways": sideways

    }


# ============================================================
# FORMAT PESAN TELEGRAM
# ============================================================

def buat_pesan(signal):

    pesan = (
        "🚨 *ABO RADAR* 🚨\n\n"
        f"*{signal['kode']}*\n"
        f"Harga : Rp {signal['harga']:,.0f}\n"
        f"MA20 : Rp {signal['ma20']:,.0f}\n"
        f"Upper BB : Rp {signal['upper']:,.0f}\n"
        f"Lower BB : Rp {signal['lower']:,.0f}\n"
        f"Bandwidth : {signal['bandwidth']*100:.2f}%\n"
        f"Volume : {signal['volume']}\n\n"
        f"🎯 Target Breakout : Rp {signal['target']:,.0f}"
    )
# ============================================================
# MEMBACA DAFTAR SAHAM
# ============================================================

def baca_daftar_saham():

    if not os.path.exists("saham_syariah.csv"):
        print("File saham_syariah.csv tidak ditemukan.")
        return []

    try:

        df = pd.read_csv("saham_syariah.csv")

        kolom = df.columns[0]

        daftar = (
            df[kolom]
            .astype(str)
            .str.strip()
            .str.upper()
            .tolist()
        )

        daftar = list(dict.fromkeys(daftar))

        return daftar

    except Exception as e:

        print(f"Gagal membaca CSV : {e}")

        return []


# ============================================================
# SCANNER
# ============================================================

def scanner():

    daftar = baca_daftar_saham()

    if len(daftar) == 0:

        kirim_telegram(
            "❌ saham_syariah.csv kosong atau tidak ditemukan."
        )

        return

    print(f"Total saham : {len(daftar)}")

    kirim_telegram(
        f"🤖 *ABO Scanner Aktif*\n\n"
        f"Memulai scan {len(daftar)} saham syariah..."
    )

    jumlah_signal = 0

    for i, kode in enumerate(daftar, start=1):

        print(f"[{i}/{len(daftar)}] {kode}")

        data = ambil_data_yahoo(kode)

        if data is None:
            continue

        hasil = cek_sideways(data)

        if hasil is None:
            continue

        if hasil["sideways"]:

            jumlah_signal += 1

            print(
                f"Signal : {kode}"
            )

            kirim_telegram(
                buat_pesan(hasil)
            )

        time.sleep(0.25)

    kirim_telegram(

        f"🏁 *ABO Scanner Selesai*\n\n"
        f"Total saham : {len(daftar)}\n"
        f"Sinyal ditemukan : {jumlah_signal}"

    )

    print("Scanner selesai.")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    scanner()
    return pesanreturn False
