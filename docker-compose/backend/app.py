from flask import Flask, jsonify
import pymysql
import os
import platform
import psutil

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "mysql")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "appdb")


def get_db():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS,
        database=DB_NAME, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "backend": "Flask", "hostname": platform.node()})


@app.route("/api/stats")
def stats():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": dict(psutil.disk_usage("/")._asdict()),
    })


@app.route("/api/visitors")
def visitors():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visitors (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(45), time DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("SELECT COUNT(*) AS total FROM visitors")
    row = cur.fetchone()
    db.close()
    return jsonify({"total_visits": row["total"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
