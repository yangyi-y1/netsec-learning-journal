from flask import Flask, jsonify, request
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
    try:
        disk_info = dict(psutil.disk_usage("/")._asdict())
    except Exception:
        disk_info = {"error": "disk info unavailable in container"}

    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": disk_info,
    })


@app.route("/api/topics")
def get_topics():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            count INT DEFAULT 0
        )
    """)
    cur.execute("SELECT id, name, count FROM topics ORDER BY id")
    topics = cur.fetchall()
    db.close()
    return jsonify(topics)


@app.route("/api/topics", methods=["POST"])
def create_topic():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name or len(name) > 100:
        return jsonify({"error": "invalid name"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO topics (name, count) VALUES (%s, 0)", (name,))
    db.commit()
    cur.execute("SELECT id, name, count FROM topics WHERE id = %s", (cur.lastrowid,))
    topic = cur.fetchone()
    db.close()
    return jsonify(topic), 201


@app.route("/api/topics/<int:topic_id>/vote", methods=["POST"])
def vote(topic_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE topics SET count = count + 1 WHERE id = %s", (topic_id,))
    if cur.rowcount == 0:
        db.close()
        return jsonify({"error": "topic not found"}), 404
    db.commit()
    cur.execute("SELECT id, name, count FROM topics WHERE id = %s", (topic_id,))
    topic = cur.fetchone()
    db.close()
    return jsonify(topic)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
