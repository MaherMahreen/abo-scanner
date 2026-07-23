"""
==========================================
ABO SCANNER
TELEGRAM ENGINE
==========================================
"""

import os
import requests


class TelegramEngine:

    def __init__(self):

        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def kirim(self, pesan):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        data = {
            "chat_id": self.chat_id,
            "text": pesan
        }

        try:

            requests.post(
                url,
                data=data,
                timeout=10
            )

        except Exception as e:

            print(e)
