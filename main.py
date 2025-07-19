from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Cache yapısı
cache = {
    "data": None,
    "timestamp": 0
}

@app.route("/")
def home():
    return "Hisse verisi API çalışıyor."

@app.route("/hisseler")
def get_hisse_data():
    now = time.time()

    # 60 saniyede bir veri çek (daha sık değil)
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
        # Eğer veri çekilemezse, cache varsa onu döner
        return jsonify({
            "status": "warning (cache - fetch failed)",
            "message": str(e),
            "data": cache["data"]
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
