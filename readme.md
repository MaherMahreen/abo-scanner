# ABO Scanner Pro

ABO Scanner Pro adalah scanner saham syariah Indonesia yang dibuat dengan Python dan dijalankan otomatis secara gratis di awan Cloud.

## Fitur Utama

- Scan massal seluruh 618 saham syariah bursa efek Indonesia
- Sideways Detector (Bollinger Bands Squeeze)
- Breakout Confirmation Detector
- Volume Spike Alert (Deteksi Bandar Masuk)
- Telegram Alert Pribadi
- GitHub Actions Automation (Berjalan Otomatis Setiap Jam 16:30 WIB)

## Struktur Berkas Repositori

- `.github/workflows/run_scanner.yml` -> Berkas otomatisasi / cron job harian bursa
- `main.py` -> Skrip pemrograman utama peluncur scanner massal bursa
- `saham_syariah.csv` -> Daftar barisan kode 618 saham syariah murni teks ke bawah
- `abo_scanner.py`, `jalan_radar.py`, `telegram.py`, `config.py` -> Berkas modul lokal cadangan proyek

## Cara Kerja

1. Sistem otomatis Actions terbangun setiap hari Senin - Jumat setelah bursa BEI tutup.
2. Membaca daftar 618 kode saham dari file `saham_syariah.csv`.
3. Mengambil data harga historis Yahoo Finance secara aman menggunakan trik jeda anti-blokir.
4. Menghitung persentase lebar volatilitas Bollinger Bands Bandwidth menggunakan rumus murni matematika.
5. Menyaring saham syariah yang sideways ketat di bawah 15% (Bandwidth <= 0.15).
6. Mengirimkan laporan sinyal bursa yang lolos sortir langsung ke akun pribadi Telegram Anda.

## Dibuat oleh

ABO Scanner Project
