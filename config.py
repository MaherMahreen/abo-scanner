"""
=========================================================
ABO SCANNER PRO
Enterprise Trading Engine for Indonesian Sharia Stocks
Configuration Center - Part 1: Core & Data Engine
Version : 2.0.0
=========================================================
"""

# =========================================================
# PROJECT IDENTITY
# =========================================================
PROJECT_NAME = "ABO Scanner Pro"
VERSION = "2.0.0"
AUTHOR = "ABO Scanner Project"
TIMEZONE = "Asia/Jakarta"
MARKET = "Indonesia"
LAST_UPDATE = "2026-07-25"

# =========================================================
# FEATURE FLAGS (GLOBAL TOGGLES)
# =========================================================
ENABLE_NEWS_ENGINE = True
ENABLE_CORPORATE_ENGINE = True
ENABLE_TELEGRAM = True
ENABLE_CACHE = True
ENABLE_LOGGING = True
ENABLE_REPORT = True
ENABLE_MARKET_FILTER = True

# =========================================================
# DATA SOURCE & DOWNLOAD ENGINE
# =========================================================
# API Redundancy Institusional: 'YAHOO' atau 'IDX_API'
PRIMARY_DATA_SOURCE = "YAHOO"
FALLBACK_DATA_SOURCE = "IDX_API"

PERIOD = "6mo"
INTERVAL = "1d"

# Wajib False agar level Support/Resistance di chart sesuai orderbook bursa riil
AUTO_ADJUST = False

# Jeda antar request (detik) untuk menghindari blokir rate limit API
REQUEST_DELAY = 1.0      
MAX_DOWNLOAD_RETRY = 3
DOWNLOAD_TIMEOUT = 30    # detik

# =========================================================
# SIDEWAYS DETECTOR
# =========================================================
SIDEWAYS_HARI = 20
SIDEWAYS_RANGE = 0.08      # 8% rentang konsolidasi harga

# =========================================================
# VOLUME ANALYSIS
# =========================================================
VOLUME_SPIKE = 2.0         # Benar-benar 2x lipat dari rata-rata volume 20 hari

# =========================================================
# BREAKOUT
# =========================================================
BREAKOUT_LOOKBACK = 20

# =========================================================
# MOVING AVERAGE (TREND FILTER)
# =========================================================
EMA_CEPAT = 20
EMA_LAMBAT = 50

# =========================================================
# RSI (MOMENTUM OSCILLATOR)
# =========================================================
RSI_PERIOD = 14
RSI_MIN = 50
RSI_MAX = 75

# =========================================================
# LIQUIDITY & MARKET RISK FILTER
# =========================================================
MIN_VALUE_TRANSACTION = 10_000_000_000   # Rp10 miliar batas bawah likuiditas harian

MARKET_INDEX = "^JKSE"  # Ticker resmi IHSG di Yahoo Finance
SHARIA_INDEX = "JII.JK"  # Ticker resmi Jakarta Islamic Index

# Mode defensif saat pasar makro melemah
DEFENSIVE_MODE = True
MAX_IHSG_DROP = -1.5     # % Batas maksimum penurunan harian IHSG

# =========================================================
# VALIDATOR (BURSA REGULATION)
# =========================================================
# Hanya memproses saham yang masuk Daftar Efek Syariah (DES)
USE_DES_ONLY = True

# Tolak saham pada Papan Pemantauan Khusus (FCA)
BLOCK_FCA = True

# Tolak saham dengan status Unusual Market Activity (UMA)
BLOCK_UMA = True

# Tolak saham dengan Notasi Khusus dari BEI
BLOCK_SPECIAL_NOTATION = True

# Papan perdagangan yang diizinkan untuk eksekusi institusional
ALLOWED_BOARD = [
    "Main Board",
    "Development Board",
]

# =========================================================
# NEWS ENGINE (NLP & SENTIMENT ANALYSIS)
# =========================================================
NEWS_MAX_AGE_HOURS = 24
NEWS_MIN_CONFIDENCE = 80
MAX_NEWS_PER_SYMBOL = 10

NEWS_SOURCES = [
    "CNBC Indonesia",
    "Kontan",
    "Bisnis Indonesia",
    "Investor Daily",
    "IDX",
]

# Kata kunci untuk pembobotan NLP Sentiment
POSITIVE_KEYWORDS = [
    "laba", "kontrak", "ekspansi", "dividen", "akuisisi", 
    "buyback", "rights issue", "stock split", "proyek baru", 
    "penjualan meningkat",
]

NEGATIVE_KEYWORDS = [
    "gagal bayar", "pailit", "PKPU", "gugatan", "sanksi", 
    "rugi", "kerugian", "penurunan laba", "delisting",
]

# =========================================================
# CORPORATE ACTION MONITORING
# =========================================================
ENABLE_CORPORATE_ACTION = True

# Jendela pemantauan taktis (Hari sebelum tanggal pelaksanaan / Cum-Date)
WATCH_DIVIDEND_DAYS = 30
WATCH_RIGHTS_ISSUE_DAYS = 30
WATCH_STOCK_SPLIT_DAYS = 14
WATCH_REVERSE_SPLIT_DAYS = 14
WATCH_BUYBACK_DAYS = 30
WATCH_MERGER_DAYS = 30
WATCH_ACQUISITION_DAYS = 30
WATCH_RUPS_DAYS = 14
WATCH_PUBLIC_EXPOSE_DAYS = 14

# =========================================================
# ABO SCORING MATRIX
# =========================================================
MIN_SCORE_ALERT = 70      # Batas bawah kelayakan (Selaras dengan Grade C)

# Grade Level
GRADE_A = 90
GRADE_B = 80
GRADE_C = 70

TOP_CANDIDATES = 5

# Distribusi Bobot Matriks 100 Poin (Total wajib = 100)
WEIGHT_TECHNICAL = 40
WEIGHT_NEWS = 25
WEIGHT_CORPORATE = 20
WEIGHT_REGIME = 15

# =========================================================
# RISK MANAGEMENT
# =========================================================
MIN_RISK_REWARD = 2.0

# ATR Multiplier untuk Dynamic SL/TP
STOPLOSS_ATR_MULTIPLIER = 2.0
TARGET_ATR_MULTIPLIER = 4.0

# Perlindungan risiko bursa harian
MAX_DAILY_LOSS_LIMIT = -10.0   # Persen batasan menjauhi area ARB harian
MAX_ATR_PERCENTAGE = 0.15      # Maksimum volatilitas harian 15% (menyaring gorengan liar)

# =========================================================
# TELEGRAM BOT INTERFACE
# =========================================================
TELEGRAM_TOKEN = ""          # Isi dengan Bot Token Anda
TELEGRAM_CHAT_ID = ""        # Isi dengan Chat ID Anda

TELEGRAM_PARSE_MODE = "HTML"
TELEGRAM_TIMEOUT = 15         # detik
TELEGRAM_RETRY = 3            # jumlah percobaan kirim ulang
TELEGRAM_BULK_SEND_DELAY = 0.05  # Jeda milidetik antar-pesan agar terhindar dari rate limit

# =========================================================
# RADAR SCHEDULER (WIB)
# =========================================================
# Jadwal Scanner Senin - Kamis
SCHEDULE_MON_THU = ["08:30", "09:30", "11:00", "12:00", "13:00", "16:15"]

# Jadwal Scanner Jumat
SCHEDULE_FRI = ["08:30", "09:30", "11:30", "12:30", "13:30", "16:15"]

# =========================================================
# DIRECTORIES & REPORTS MANAGEMENT
# =========================================================
CACHE_FOLDER = "cache"
LOG_FOLDER = "logs"
REPORT_FOLDER = "reports"

# Masa berlaku data dalam cache (detik)
PRICE_CACHE_EXPIRE = 900       # 15 menit
NEWS_CACHE_EXPIRE = 1800       # 30 menit
CORPORATE_CACHE_EXPIRE = 86400 # 24 jam

SCANNER_LOG = "scanner.log"
ERROR_LOG = "error.log"
TELEGRAM_LOG = "telegram.log"
LOG_LEVEL = "INFO"

SAVE_REPORT = True
SAVE_CSV = True
SAVE_HTML = False

# =========================================================
# AUTOMATIC VALIDATION RUNNER
# =========================================================
# Sistem perlindungan berlapis agar engine langsung mati saat booting jika total bobot salah
TOTAL_WEIGHT = WEIGHT_TECHNICAL + WEIGHT_NEWS + WEIGHT_CORPORATE + WEIGHT_REGIME
if TOTAL_WEIGHT != 100:
    raise ValueError(f"[CONFIG ERROR] Total bobot ABO Scoring Matrix harus tepat 100 poin! (Saat ini: {TOTAL_WEIGHT})")
