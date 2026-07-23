def kirim_radar_telegram(pesan):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN_LANGSUNG}/sendMessage"

    payload = {
        "chat_id": CHAT_ID_LANGSUNG,
        "text": pesan,
        "parse_mode": "Markdown"
    }

    try:

        response = requests.post(
            url,
            data=payload,
            timeout=20
        )

        print(response.status_code)
        print(response.text)

        return response.status_code == 200

    except Exception as e:

        print("Gagal kirim Telegram:", e)

        return False