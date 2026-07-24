"""
=========================================================
ABO SCANNER PRO
Enterprise Trading Engine for Indonesian Sharia Stocks
Configuration Center
Version : 2.0.0
=========================================================
"""

# =========================================================
# PROJECT
# =========================================================

PROJECT_NAME = "ABO Scanner Pro"
VERSION = "2.0.0"
AUTHOR = "ABO Scanner Project"
TIMEZONE = "Asia/Jakarta"
MARKET = "Indonesia"


# =========================================================
# SIDEWAYS DETECTOR
# =========================================================

SIDEWAYS_HARI = 20
SIDEWAYS_RANGE = 0.08      # 8%

# =========================================================
# VOLUME ANALYSIS
# =========================================================

VOLUME_SPIKE = 1.5         # 2x rata-rata 20 hari

# =========================================================
# BREAKOUT
# =========================================================

BREAKOUT_LOOKBACK = 20

# =========================================================
# MOVING AVERAGE
# =========================================================

EMA_CEPAT = 20
EMA_LAMBAT = 50

# =========================================================
# RSI
# =========================================================

RSI_PERIOD = 14
RSI_MIN = 50
RSI_MAX = 75

# =========================================================
# LIQUIDITY FILTER
# =========================================================

MIN_VALUE_TRANSACTION = 10_000_000_000   # Rp10 miliar


# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_TOKEN = ""          # Isi dengan Bot Token Anda
TELEGRAM_CHAT_ID = ""        # Isi dengan Chat ID Anda

TELEGRAM_PARSE_MODE = "HTML"
TELEGRAM_TIMEOUT = 15         # detik
TELEGRAM_RETRY = 3            # jumlah percobaan kirim ulang

# =========================================================
# SCHEDULER
# =========================================================


# Jadwal Scanner Senin - Kamis
SCHEDULE_MON_THU = [
    "08:30",
    "09:30",
    "11:00",
    "12:00",
    "13:00",
    "16:15",
]

# Jadwal Scanner Jumat
SCHEDULE_FRI = [
    "08:30",
    "09:30",
    "11:30",
    "12:30",
    "13:30",
    "16:15",
]

# =========================================================
# DATA DOWNLOAD
# =========================================================

# Periode dan interval data Yahoo Finance
PERIOD = "6mo"
INTERVAL = "1d"

# Menggunakan harga yang sudah disesuaikan (stock split/dividen)
AUTO_ADJUST = True

# Jeda antar request untuk menghindari rate limit
REQUEST_DELAY = 1.0      # detik

# Jumlah maksimum percobaan download ulang
MAX_DOWNLOAD_RETRY = 3

# Timeout koneksi
DOWNLOAD_TIMEOUT = 30    # detik


# =========================================================
# CACHE
# =========================================================

CACHE_FOLDER = "cache"

# Masa berlaku cache
PRICE_CACHE_EXPIRE = 900      # 15 menit
NEWS_CACHE_EXPIRE = 1800      # 30 menit
CORPORATE_CACHE_EXPIRE = 86400    # 24 jam


# =========================================================
# LOGGING
# =========================================================


LOG_FOLDER = "logs"

SCANNER_LOG = "scanner.log"
ERROR_LOG = "error.log"
TELEGRAM_LOG = "telegram.log"

LOG_LEVEL = "INFO"


# =========================================================
# VALIDATOR
# =========================================================

# Hanya memproses saham yang masuk Daftar Efek Syariah (DES)
USE_DES_ONLY = True

# Tolak saham pada Papan Pemantauan Khusus (FCA)
BLOCK_FCA = True

# Tolak saham dengan status Unusual Market Activity (UMA)
BLOCK_UMA = True

# Tolak saham dengan Notasi Khusus
BLOCK_SPECIAL_NOTATION = True

# Papan perdagangan yang diizinkan
ALLOWED_BOARD = [
    "Main Board",
    "Development Board",
]

# =========================================================
# MARKET FILTER
# =========================================================

# Aktifkan filter kondisi pasar
ENABLE_MARKET_FILTER = True

# Indeks acuan
MARKET_INDEX = "IHSG"
SHARIA_INDEX = "JII"

# Mode defensif saat pasar melemah
DEFENSIVE_MODE = True

# Batas maksimum penurunan IHSG harian (%)
MAX_IHSG_DROP = -1.5

# Jumlah kandidat maksimum yang dikirim ke Telegram
TOP_CANDIDATES = 5

# =========================================================
# FEATURE FLAGS
# =========================================================

ENABLE_NEWS_ENGINE = True
ENABLE_CORPORATE_ENGINE = True
ENABLE_TELEGRAM = True
ENABLE_CACHE = True
ENABLE_LOGGING = True
ENABLE_REPORT = True

# =========================================================
# NEWS ENGINE
# =========================================================

# Maksimum umur berita (jam)
NEWS_MAX_AGE_HOURS = 24

# Minimum confidence berita (%)
NEWS_MIN_CONFIDENCE = 80

# Maksimum jumlah berita yang dianalisis per saham
MAX_NEWS_PER_SYMBOL = 10

# Sumber berita terpercaya
NEWS_SOURCES = [
    "CNBC Indonesia",
    "Kontan",
    "Bisnis Indonesia",
    "Investor Daily",
    "IDX",
]

# Kata kunci positif
POSITIVE_KEYWORDS = [
    "laba",
    "kontrak",
    "ekspansi",
    "dividen",
    "akuisisi",
    "buyback",
    "rights issue",
    "stock split",
    "proyek baru",
    "penjualan meningkat",
]

# Kata kunci negatif
NEGATIVE_KEYWORDS = [
    "gagal bayar",
    "pailit",
    "PKPU",
    "gugatan",
    "sanksi",
    "rugi",
    "kerugian",
    "penurunan laba",
    "delisting",
]

# =========================================================
# CORPORATE ACTION
# =========================================================

# Aktifkan pemantauan Corporate Action
ENABLE_CORPORATE_ACTION = True

# Jendela pemantauan (hari sebelum kejadian)
WATCH_DIVIDEND_DAYS = 90
WATCH_RIGHTS_ISSUE_DAYS = 90
WATCH_STOCK_SPLIT_DAYS = 90
WATCH_REVERSE_SPLIT_DAYS = 90
WATCH_BUYBACK_DAYS = 90
WATCH_MERGER_DAYS = 90
WATCH_ACQUISITION_DAYS = 90
WATCH_RUPS_DAYS = 90
WATCH_PUBLIC_EXPOSE_DAYS = 90


# =========================================================
# ABO SCORING
# =========================================================

# Skor minimum agar saham masuk kandidat
MIN_SCORE_ALERT = 80

# Grade Scanner
GRADE_A = 90
GRADE_B = 80
GRADE_C = 70


# =========================================================
# RISK MANAGEMENT
# =========================================================

# Risk Reward Ratio Minimum
MIN_RISK_REWARD = 2.0

# ATR Multiplier
STOPLOSS_ATR_MULTIPLIER = 2.0
TARGET_ATR_MULTIPLIER = 4.0

# =========================================================
# REPORT
# =========================================================

REPORT_FOLDER = "reports"

SAVE_REPORT = True
SAVE_CSV = True
SAVE_HTML = False

# =========================================================
# VERSION INFO
# =========================================================

LAST_UPDATE = "2026-07-25"