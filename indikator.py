"""
==========================================
ABO SCANNER
INDIKATOR
==========================================
"""

import pandas as pd


def ema(df, periode):

    return df["Close"].ewm(
        span=periode,
        adjust=False
    ).mean()


def sma(df, periode):

    return df["Close"].rolling(
        periode
    ).mean()


def volume_rata(df, periode=20):

    return df["Volume"].rolling(
        periode
    ).mean()


def nilai_transaksi(df):

    return df["Close"] * df["Volume"]


def highest(df, periode=20):

    return df["High"].rolling(
        periode
    ).max()


def lowest(df, periode=20):

    return df["Low"].rolling(
        periode
    ).min()


def range_sideways(df, periode=20):

    high = highest(df, periode)

    low = lowest(df, periode)

    return (high - low) / low
