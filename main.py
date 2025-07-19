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


from datetime import datetime, timedelta

def is_borsa_open():
    now_utc = datetime.utcnow()
    now_tr = now_utc + timedelta(hours=3)  # Türkiye UTC+3

    if now_tr.weekday() >= 5:  # Cumartesi veya Pazar
        return False

    if now_tr.hour < 10 or now_tr.hour >= 19:
        return False

    return True


@app.route("/")
def home():
    return "Hisse verisi API çalışıyor."

@app.route("/hisseler")
def get_hisse_data():
    now = time.time()

    # Eğer borsa kapalıysa cache'i döndür
    if not is_borsa_open():
        return jsonify({
            "status": "success (cache only - market closed)",
            "data": cache["data"]
        })

    # 60 saniyeden az süre geçtiyse cache kullan
    if now - cache["timestamp"] < 60 and cache["data"] is not None:
        return jsonify({
            "status": "success (cache)",
            "data": cache["data"]
        })

    # Yeni veri çekmeye çalış
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
        # Veri çekilemezse cache varsa onu döndür
        return jsonify({
            "status": "warning (cache - fetch failed)",
            "message": str(e),
            "data": cache["data"]
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
