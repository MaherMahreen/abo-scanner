"""
==========================================
ABO SCANNER PRO
MAIN PROGRAM
==========================================
"""

import traceback

from scanner import Scanner
from telegram import TelegramEngine


def main():
    try:
        scanner = Scanner()

        hasil = scanner.scan()

        if len(hasil) == 0:
            print("Tidak ada saham yang memenuhi kriteria.")
            return

        pesan = "🔥 ABO SCANNER PRO\n\n"
        pesan += f"Total Kandidat : {len(hasil)}\n\n"
        pesan += "TOP 20\n\n"

        for i, item in enumerate(hasil[:20], start=1):
            alasan = ", ".join(item["alasan"])

            pesan += (
                f"{i}. {item['kode']}\n"
                f"Score : {item['score']}\n"
                f"{alasan}\n\n"
            )

        print(pesan)
        TelegramEngine().kirim(pesan)

    except Exception:
        print("===== ERROR =====")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
