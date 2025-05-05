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

# Asıl kontrol fonksiyonu: "Arkadan Çekiş" ifadesini arar
def check_for_arkadan_cekis():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(TESLA_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # "arkadan çekiş" ve diğer terimleri kontrol et
            if "arkadan çekiş" in text or \
               "model y arkadan" in text or \
               "model y rear-wheel drive" in text:
                return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return False
# Telegram mesajını gönderme fonksiyonu
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

# Sürekli çalışan arka plan görevi
def background_worker():
    print("Tesla 'Arkadan Çekiş' kontrolü başlatıldı...")
    while True:
        print("Kontrol ediliyor...")
        if check_for_rear_wheel_drive():
            send_telegram_message("🚗 Tesla Model Y 'Arkadan Çekiş' stokta! Kontrol et: " + TESLA_URL)
        time.sleep(10)  # 10 saniye bekle ve tekrar kontrol et

# Web servis
@app.route('/')
def index():
    return "Tesla checker is running."

# Ana uygulama çalıştırma
if __name__ == '__main__':
    threading.Thread(target=background_worker).start()  # Sonsuz döngüyü başlat
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
