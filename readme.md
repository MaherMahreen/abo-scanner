# 🚀 ABO Scanner Pro

## Enterprise Trading Engine for Indonesian Sharia Stocks

ABO Scanner Pro adalah sistem **Enterprise Trading Engine** untuk melakukan penyaringan (screening) saham syariah Indonesia secara otomatis berdasarkan metode **Converging Evidence**.

Scanner ini menggabungkan analisis teknikal, likuiditas, aksi korporasi, berita fundamental, kondisi pasar, serta validasi regulasi sehingga menghasilkan daftar saham dengan probabilitas momentum yang lebih tinggi dan meminimalkan keputusan yang bersifat spekulatif.

---

# 🎯 Tujuan Proyek

ABO Scanner Pro dirancang untuk:

- Menyaring seluruh saham syariah yang terdaftar dalam Daftar Efek Syariah (DES) terbaru.
- Menghilangkan saham dengan risiko tinggi (FCA, Notasi Khusus, UMA, dan lainnya).
- Mengidentifikasi momentum sebelum menjadi perhatian mayoritas pasar.
- Mengirimkan notifikasi otomatis ke Telegram sesuai jadwal Bursa Efek Indonesia.
- Menjadi sistem screening modular yang mudah dikembangkan dan dipelihara.

---

# 📌 Filosofi Scanner

Scanner dibangun berdasarkan lima prinsip utama:

- ✅ Syariah First
- ✅ Converging Evidence
- ✅ Zero Speculation
- ✅ Capital Preservation
- ✅ Modular Architecture

---

# ⚙️ Fitur Utama

- Scan seluruh saham syariah Indonesia (DES terbaru)
- Validasi legalitas dan status perdagangan emiten
- Sideways Detector (Bollinger Bands Squeeze)
- Breakout Confirmation
- EMA Trend Analysis
- Highest 20 Breakout
- Volume Spike Detection
- Liquidity Filter
- Frequency Trade Validation
- Market Regime Filter (IHSG & JII)
- News Sentiment Analysis
- Corporate Action Monitoring
- Dynamic Target Price
- Dynamic Stop Loss
- Telegram Premium Notification
- GitHub Actions Automation
- Error Logging
- Cache System

---

# 📂 Struktur Proyek

```
.github/
│
├── workflows/
│
├── cache/
│
├── logs/
│
├── reports/
│
├── data_source/
│   ├── ojk.py
│   ├── yahoo.py
│   └── idx.py
│
├── config.py
├── validator.py
├── data.py
├── indicator.py
├── corporate.py
├── news.py
├── score.py
├── report.py
├── telegram.py
├── main.py
├── jalan_radar.py
├── abo_scanner.py
├── saham_syariah.csv
├── requirements.txt
└── README.md
```

---

# 🔄 Workflow Scanner

Scheduler

↓

Validasi Saham Syariah

↓

Unduh Data Bursa

↓

Validasi Regulasi

↓

Perhitungan Indikator

↓

Corporate Action Filter

↓

News Validation

↓

Momentum Scoring

↓

Pembuatan Report

↓

Telegram Notification

---

# 📊 Data yang Digunakan

## Regulasi

- Daftar Efek Syariah (DES)
- IDX Board
- Notasi Khusus
- UMA
- FCA

## Data Pasar

- OHLCV
- Volume
- Nilai Transaksi
- Frekuensi Transaksi
- IHSG
- JII

## Corporate Action

- Dividen
- Rights Issue
- Stock Split
- Reverse Split
- Buyback
- Akuisisi
- Merger
- RUPS
- Public Expose

## Berita

- Berita fundamental
- Sentimen positif
- Sentimen negatif
- Confidence Validation
- Freshness Check

---

# ⏰ Jadwal Scanner

Scanner berjalan otomatis pada hari bursa:

- 08:30 WIB
- 09:30 WIB
- 11:00 WIB (Senin–Kamis)
- 11:30 WIB (Jumat)
- 12:00 WIB (Senin–Kamis)
- 12:30 WIB (Jumat)
- 13:00 WIB (Senin–Kamis)
- 13:30 WIB (Jumat)
- 16:15 WIB

---

# 📱 Output

Setiap jadwal scanner akan menghasilkan:

- Ringkasan kondisi pasar
- Daftar Top Momentum
- Skor masing-masing saham
- Alasan kelolosan
- Target Price
- Stop Loss
- Ringkasan berita
- Informasi Corporate Action
- Waktu pemindaian

Seluruh laporan dikirim otomatis ke Telegram.

---

# 🛡️ Prinsip Keamanan

ABO Scanner Pro tidak hanya mencari peluang, tetapi juga berusaha mengurangi risiko dengan:

- Filter saham syariah
- Filter likuiditas
- Filter regulasi
- Filter berita
- Filter corporate action
- Filter market regime
- Logging system
- Cache system
- Retry mechanism

---

# 🚀 Roadmap

Versi 2.x

- Enterprise Modular Architecture
- News Engine
- Corporate Engine
- Validator Engine
- Dynamic Scoring
- Premium Telegram Report

Versi berikutnya

- Backtesting Engine
- Portfolio Monitoring
- Watchlist Management
- Dashboard Performance
- AI Sentiment Analysis

---

# 👨‍💻 Dibuat Oleh

**ABO Scanner Project**

Enterprise Trading Engine for Indonesian Sharia Stocks

Versi: **2.0.0**