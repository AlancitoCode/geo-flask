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
    ts  = data.get("ts") or datetime.datetime.utcnow().isoformat()
    lat = data.get("lat")
    lon = data.get("lon")

    os.makedirs("data", exist_ok=True)
    path = "data/geo.csv"
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, lat, lon])

    print("[geo-capture]", ts, lat, lon)  # lo verás en la consola
    return jsonify(ok=True, saved={"ts": ts, "lat": lat, "lon": lon})

@app.get("/last")
def last():
    path = "data/geo.csv"
    if not os.path.exists(path):
        return jsonify(error="Aún no hay registros"), 404
    *_, last_line = open(path, encoding="utf-8").read().strip().splitlines()
    return jsonify(last=last_line)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa PORT
    app.run(host="0.0.0.0", port=port, debug=False)
