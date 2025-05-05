import requests
from bs4 import BeautifulSoup
import threading
import time
from flask import Flask
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TESLA_URL = 'https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34025&range=0'

# Test Modu: Her zaman True döner, her 30 saniyede bir mesaj alırsın.
def check_for_rear_wheel_drive():
    # TEST: Her zaman True dönüyoruz, böylece her 30 saniyede bir bildirim gelir.
    return True

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

def background_worker():
    print("Tesla 'Arkadan Çekiş' kontrolü başlatıldı...")
    while True:
        print("Kontrol ediliyor...")
        if check_for_rear_wheel_drive():
            send_telegram_message("🚗 Tesla Model Y 'Arkadan Çekiş' stokta! Kontrol et: " + TESLA_URL)
        time.sleep(30)  # 30 saniye bekle ve tekrar kontrol et

@app.route('/')
def index():
    return "Tesla checker is running."

if __name__ == '__main__':
    threading.Thread(target=background_worker).start()  # Sonsuz döngüyü başlat
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
