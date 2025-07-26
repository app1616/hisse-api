from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Çoklu veri tipi için cache sistemi
cache = {}

# API sabit başlıklar
API_KEY = "apikey 7prp30z5o7rvwLKCDXvbz1:1wVCAlfEBk6ixz2p296ouX"
HEADERS = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

# Türlere göre endpointler (şimdilik boş, sen vereceksin)
ENDPOINTLER = {
    "hisse": "https://api.collectapi.com/economy/hisseSenedi",
    "doviz": "https://api.collectapi.com/economy/allCurrency",
    "altin": "https://api.collectapi.com/economy/goldPrice",
    "kripto": "https://api.collectapi.com/economy/cripto",
    "emtia": "https://api.collectapi.com/economy/emtia"
}

@app.route("/")
def home():
    return "Finans verisi API çalışıyor."

@app.route("/veri")
def get_veri():
    tur = request.args.get("tur")

    if not tur or tur not in ENDPOINTLER:
        return jsonify({
            "status": "error",
            "message": "Geçersiz veya eksik 'tur' parametresi. Örnek: /veri?tur=hisse"
        }), 400

    now = time.time()
    cache_key = f"{tur}_cache"

    # Cache kontrolü
    if cache_key in cache and now - cache[cache_key]["timestamp"] < 150:
        return jsonify({
            "status": "success (cache)",
            "data": cache[cache_key]["data"]
        })

    # Yeni veri çekme
    try:
        response = requests.get(ENDPOINTLER[tur], headers=HEADERS)
        data = response.json()
        cache[cache_key] = {
            "data": data,
            "timestamp": now
        }
        return jsonify({
            "status": "success (fresh)",
            "data": data
        })
    except Exception as e:
        return jsonify({
            "status": "warning (cache - fetch failed)",
            "message": str(e),
            "data": cache.get(cache_key, {}).get("data")
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
