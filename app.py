from flask import Flask, request, send_file, make_response
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "opens.log"
PIXEL_FILE = "pixel.png"

@app.route("/")
def home():
    return "<h3>Email Tracker is running ✅</h3><p>Use /open?id=yourid</p>"

@app.route("/open")
def open_tracker():
    # --- Get headers safely ---
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        # X-Forwarded-For may contain multiple IPs -> take the first (client)
        real_ip = forwarded_for.split(",")[0].strip()
    else:
        real_ip = request.remote_addr

    ua = request.headers.get("User-Agent", "-")
    referer = request.headers.get("Referer", "-")
    track_id = request.args.get("id", "-")

    # --- Log event ---
    log_line = (
        f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
        f"id={track_id} | ip={real_ip} | "
        f"ua=\"{ua}\" | referer=\"{referer}\" | "
        f"xfwd=\"{forwarded_for}\"\n"
    )
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    # --- Return the transparent pixel with no-cache headers ---
    resp = make_response(send_file(PIXEL_FILE, mimetype="image/png"))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.route("/logs")
def show_logs():
    if not os.path.exists(LOG_FILE):
        return "<pre>No logs yet.</pre>"
    with open(LOG_FILE) as f:
        content = f.read()
    # Display in HTML-safe <pre> format
    return (
        "<h3>Open Events</h3>"
        "<pre style='white-space:pre-wrap; font-family:monospace;'>"
        + content +
        "</pre>"
    )

if __name__ == "__main__":
    # Bind to all interfaces (needed for Render)
    app.run(host="0.0.0.0", port=5000)
