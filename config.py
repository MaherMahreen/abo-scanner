"""
====================================
ABO SCANNER CONFIG
====================================
"""

# Data
PERIOD = "6mo"
INTERVAL = "1d"

# Sideways
SIDEWAYS_HARI = 20
SIDEWAYS_RANGE = 0.08      # 8%

# Volume
VOLUME_SPIKE = 2.0         # 2x rata-rata 20 hari

# Breakout
BREAKOUT_LOOKBACK = 20

# Moving Average
EMA_CEPAT = 20
EMA_LAMBAT = 50

# RSI
RSI_PERIOD = 14
RSI_MIN = 50
RSI_MAX = 70

# Money Flow (indikasi)
MIN_VALUE_TRANSACTION = 10_000_000_000  # Rp10 miliar

# ABO Score
MIN_SCORE_ALERT = 80
