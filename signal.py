"""
==========================================
ABO SCANNER
SIGNAL ENGINE
==========================================
"""

from indikator import (
    ema,
    volume_rata,
    highest,
    range_sideways,
    nilai_transaksi
)

from config import (
    SIDEWAYS_HARI,
    SIDEWAYS_RANGE,
    BREAKOUT_LOOKBACK,
    VOLUME_SPIKE,
    EMA_CEPAT,
    EMA_LAMBAT,
    MIN_VALUE_TRANSACTION
)


class SignalEngine:

    def cek_sideways(self, df):
        nilai = range_sideways(df, SIDEWAYS_HARI).iloc[-1]
        return nilai <= SIDEWAYS_RANGE

    def cek_breakout(self, df):
        resistance = highest(df, BREAKOUT_LOOKBACK).shift(1)
        return df["Close"].iloc[-1] > resistance.iloc[-1]

    def cek_volume(self, df):
        rata = volume_rata(df)
        return df["Volume"].iloc[-1] > rata.iloc[-1] * VOLUME_SPIKE

    def cek_ema(self, df):
        ema20 = ema(df, EMA_CEPAT)
        ema50 = ema(df, EMA_LAMBAT)
        return ema20.iloc[-1] > ema50.iloc[-1]

    def cek_transaksi(self, df):
        transaksi = nilai_transaksi(df)
        return transaksi.iloc[-1] >= MIN_VALUE_TRANSACTION
