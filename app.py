from flask import Flask, send_file, request, jsonify, redirect
import csv, datetime, os

app = Flask(__name__)

@app.route("/")
def root():
    return redirect("/geo.html")

@app.route("/geo.html")
def geo_page():
    if not os.path.exists("geo.html"):
        return "geo.html no encontrado en esta carpeta", 500
    return send_file("geo.html")

@app.post("/geo-capture")
def geo_capture():
    try:
        data = request.get_json(force=True)
    except Exception:
        data = {}
    ts  = data.get("ts") or datetime.datetime.utcnow().isoformat()
    lat = data.get("lat")
    lon = data.get("lon")

    os.makedirs("data", exist_ok=True)
    path = "data/geo.csv"
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, lat, lon])

    print("[geo-capture]", ts, lat, lon, "raw:", data)  # <-- lo verás en la terminal
    return jsonify({"ok": True, "saved": {"ts": ts, "lat": lat, "lon": lon}})

# Rutas de diagnóstico
@app.get("/health")
def health():
    return jsonify(ok=True)

@app.get("/last")
def last():
    path = "data/geo.csv"
    if not os.path.exists(path):
        return jsonify(error="Aún no hay registros"), 404
    *_, last_line = open(path, encoding="utf-8").read().strip().splitlines()
    return jsonify(last=last_line)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
