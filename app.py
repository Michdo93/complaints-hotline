import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory, request

app = Flask(__name__)

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", config=config)

@app.route("/api/complaints", methods=["GET"])
def get_complaints():
    config = load_config()
    records_folder = config.get("records_folder", "recordoffs")
    datetime_format = config.get("datetime_format", "%Y-%m-%d_%H-%M-%S")
    
    complaints = []
    if os.path.exists(records_folder):
        for filename in os.listdir(records_folder):
            if filename.endswith(".wav"):
                basename = os.path.splitext(filename)[0]
                try:
                    dt = datetime.strptime(basename, datetime_format)
                    complaints.append({
                        "filename": filename,
                        "date": dt.strftime("%Y-%m-%d"),
                        "time": dt.strftime("%H:%M:%S"),
                        "timestamp": dt.timestamp()
                    })
                except ValueError:
                    continue

    complaints.sort(key=lambda x: x["timestamp"], reverse=True)
    return jsonify(complaints)

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    config = load_config()
    records_folder = config.get("records_folder", "recordoffs")
    return send_from_directory(records_folder, filename)

@app.route("/api/complaints/<filename>", methods=["DELETE"])
def delete_complaint(filename):
    config = load_config()
    records_folder = config.get("records_folder", "recordoffs")
    file_path = os.path.join(records_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True, "message": "File deleted successfully"})
    return jsonify({"success": False, "message": "File not found"}), 404

if __name__ == "__main__":
    cfg = load_config()
    host = cfg.get("web", {}).get("host", "0.0.0.0")
    port = cfg.get("web", {}).get("port", 5000)
    app.run(host=host, port=port, debug=False)