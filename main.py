from flask import Flask, jsonify
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Cache yapısı
cache = {
    "data": None,
    "timestamp": 0
}

# Borsa açık mı kontrolü
def is_borsa_open():
    now = datetime.now()
    if now.weekday() >= 5:  # Cumartesi, Pazar
        return False
    if now.hour < 10 or now.hour >= 22:
        return False
    return True

@app.route("/")
def home():
    return "Hisse verisi API çalışıyor."

@app.route("/hisseler")
def get_hisse_data():
    now = time.time()

    # Borsa kapalıysa sadece cache göster
    if not is_borsa_open():
        return jsonify({
            "status": "success (cache only - market closed)",
            "data": cache["data"]
        })

    # Eğer 10 saniyeden az geçtiyse tekrar veri çekme
    if now - cache["timestamp"] < 60 and cache["data"] is not None:
        return jsonify({
            "status": "success (cache)",
            "data": cache["data"]
        })

    # Yeni veri çek
    try:
        response = requests.get(
            "https://api.collectapi.com/economy/hisseSenedi",
            headers={
                "authorization": "apikey 0cQkwDtbKDzPtLo5Tn5u9P:7epmAa4z3GfPFnDpsIvN4G",  # ← BURAYI DOLDUR
                "content-type": "application/json"
            }
        )
        data = response.json()
        cache["data"] = data
        cache["timestamp"] = now
        return jsonify({
            "status": "success (fresh)",
            "data": data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": cache["data"]
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
