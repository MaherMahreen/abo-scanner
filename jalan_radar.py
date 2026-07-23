def kirim_radar_telegram(pesan):

    url = f"https://api.telegram.org/bot8567909596:AAFFLsu_Nh6-WCuZbb5F73cts-VUbWBaC5A

/sendMessage"

    payload = {
        "chat_id": 8690860489,
        "text": pesan
    }

    try:
        response = requests.post(
            url,
            data=payload,
            timeout=20
        )

        print("URL :", url)
        print("Status :", response.status_code)
        print("Response :", response.text)

        return response.status_code == 200

    except Exception as e:
        print("Gagal:", e)
        return False