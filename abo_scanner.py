"""
==========================================
ABO SCANNER
MAIN SCANNER ENGINE
Version 2.0
==========================================
"""

from data import DataEngine
from signal import SignalEngine
from score import ScoreEngine


class Scanner:

    def __init__(self):

        self.data = DataEngine()
        self.signal = SignalEngine()

    def scan(self):

        hasil = []

        semua = self.data.ambil_semua()

        print(f"\nTotal saham berhasil dibaca : {len(semua)}\n")

        for kode, df in semua.items():

            score = ScoreEngine()

            try:

                if self.signal.cek_sideways(df):
                    score.tambah(25, "Sideways")

                if self.signal.cek_breakout(df):
                    score.tambah(20, "Breakout")

                if self.signal.cek_volume(df):
                    score.tambah(20, "Volume Spike")

                if self.signal.cek_ema(df):
                    score.tambah(10, "EMA Bullish")

                if self.signal.cek_transaksi(df):
                    score.tambah(15, "Nilai Transaksi Besar")

                hasil.append({
                    "kode": kode,
                    "score": score.hasil()["score"],
                    "alasan": score.hasil()["alasan"]
                })

            except Exception as e:

                print(kode, e)

        hasil = sorted(
            hasil,
            key=lambda x: x["score"],
            reverse=True
        )

        return hasil
