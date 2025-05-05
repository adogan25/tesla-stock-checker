# main.py
# import requests
from bs4 import BeautifulSoup
import time

# Telegram ayarları
TELEGRAM_TOKEN = '7770662830:AAF81ZmkPNNCxV2sUg-0jSVyEb64fTNkBn8'
TELEGRAM_CHAT_ID = '1476078120'

# Tesla sayfa URL'si
TESLA_URL = 'https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34025&range=0'

def check_for_standard_range():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(TESLA_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            if "standart menzil" in text:
                return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram bildirimi gönderilemedi: {e}")

def main():
    print("Tesla Standart Menzil kontrolü başlatıldı...")
    while True:
        print("Kontrol ediliyor...")
        if check_for_standard_range():
            send_telegram_message("🚨 Tesla Model Y Standart Menzil stokta! Hemen bak: " + TESLA_URL)
            break  # Bildirim gönderildikten sonra döngüyü durdur
        time.sleep(10)  # 30 saniyede bir kontrol

if __name__ == "__main__":
    main()
