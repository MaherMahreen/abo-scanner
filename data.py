"""
====================================================
ABO SCANNER
Data Engine v1.0
====================================================
Fungsi:
- Membaca daftar saham dari saham_syariah.csv
- Mengambil data OHLCV dari Yahoo Finance
- Mengembalikan DataFrame untuk dianalisis
====================================================
"""

import pandas as pd
import yfinance as yf


class DataEngine:

    def __init__(self):
        self.file_saham = "saham_syariah.csv"

    def daftar_saham(self):

        try:

            data = pd.read_csv(self.file_saham)

            return data["kode"].dropna().tolist()

        except Exception as e:

            print("Gagal membaca daftar saham")
            print(e)

            return []

    def ambil_data(
        self,
        kode,
        period="6mo",
        interval="1d"
    ):

        ticker = f"{kode}.JK"

        try:

            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False,
                threads=False
            )

            if df.empty:
                return None

            df = df.reset_index()

            df["Kode"] = kode

            return df

        except Exception as e:

            print(f"{kode} : {e}")

            return None

    def ambil_semua(
        self,
        period="6mo",
        interval="1d"
    ):

        hasil = {}

        daftar = self.daftar_saham()

        print(f"Jumlah saham : {len(daftar)}")

        for i, kode in enumerate(daftar):

            print(f"[{i+1}/{len(daftar)}] {kode}")

            data = self.ambil_data(
                kode,
                period,
                interval
            )

            if data is not None:
                hasil[kode] = data

        return hasil
