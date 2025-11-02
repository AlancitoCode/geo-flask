from flask import Flask, send_file, request, jsonify, redirect
from flask_cors import CORS
import csv, datetime, os

app = Flask(__name__)
CORS(app, resources={r"/geo-capture": {"origins": "*"}})

@app.route("/")
def root():
    return redirect("/geo.html")

@app.route("/geo.html")
def geo_page():
    return send_file("geo.html")

@app.post("/geo-capture")
def geo_capture():
    data = request.get_json(force=True)
    ts = data.get("ts") or datetime.datetime.utcnow().isoformat()
    lat = data.get("lat")
    lon = data.get("lon")
    os.makedirs("data", exist_ok=True)
    with open("data/geo.csv","a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, lat, lon])
    return jsonify(ok=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render te da PORT
    app.run(host="0.0.0.0", port=port, debug=False)
