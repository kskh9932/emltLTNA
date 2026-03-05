from flask import Flask, request, send_file
from datetime import datetime

app = Flask(__name__)

@app.route("/open")
def open_tracker():
    with open("opens.log", "a") as f:
        f.write(f"{datetime.now()} | IP: {request.remote_addr} | "
                f"UA: {request.headers.get('User-Agent')} | "
                f"ID: {request.args.get('id')}\n")
    return send_file("pixel.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

