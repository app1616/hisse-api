from flask import Flask, jsonify
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Cache yapısı
cache = {
    "data": None,
    "timestamp": 0
}

# Türkiye saatine göre borsa açık mı kontrolü
def is_borsa_open():
    return True


@app.route("/")
def home():
    return "Hisse verisi API çalışıyor."

@app.route("/hisseler")
def get_hisse_data():
    now = time.time()

    if not is_borsa_open():
        return jsonify({
            "status": "success (cache only - market closed)",
            "data": cache["data"]
        })

    if now - cache["timestamp"] < 60 and cache["data"] is not None:
        return jsonify({
            "status": "success (cache)",
            "data": cache["data"]
        })

    try:
        response = requests.get(
            "https://api.collectapi.com/economy/hisseSenedi",
            headers={
                "authorization": "apikey 0cQkwDtbKDzPtLo5Tn5u9P:7epmAa4z3GfPFnDpsIvN4G",
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
