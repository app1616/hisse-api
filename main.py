from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Çoklu veri tipi için cache sistemi
cache = {}

# API sabit başlıklar
API_KEY = "apikey 0P0ogqIBxo2usYWcj5WNID:6ntAJIO9CNNqda"
HEADERS = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

# Türlere göre endpointler (şimdilik boş, sen vereceksin)
ENDPOINTLER = {
    "hisse": "https://api.collectapi.com/economy/hisseSenedi",
    "doviz": "https://finance.truncgil.com/api/currency-rates",
    "altin": "https://finance.truncgil.com/api/gold-rates",
    "kripto": "https://finance.truncgil.com/api/crypto-currency-rates",
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
    if cache_key in cache and now - cache[cache_key]["timestamp"] < 1250:
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
