# Import
import os
import secrets
import math
import threading
import zoneinfo

from time import gmtime, strftime
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

load_dotenv()

### 
# Config
###

LOGIN_PASSWORD  = os.getenv("LOGIN_PASSWORD", secrets.token_hex(64))
SECRET_KEY      = os.getenv("SECRET_KEY", secrets.token_hex(32))
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME", "twitchdev")
WEBSITE_DOMAIN  = os.getenv("WEBSITE_DOMAIN", "localhost")

app = Flask(__name__, template_folder="template", static_folder="static", static_url_path="/static")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
app.secret_key = SECRET_KEY
 
###
# Var
###
messages_lock = threading.Lock()
listMessages = [{"id": 0, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 1, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 2, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 3, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 4, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 5, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 6, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 7, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 8, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 9, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 10, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 11, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 12, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 13, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 14, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 15, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 16, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 17, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 18, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 19, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 20, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 21, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 22, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 23, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 24, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 25, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 26, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 27, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 28, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 29, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 30, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 31, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 32, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 33, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 34, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 35, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 36, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 37, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 38, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 39, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 40, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 41, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 42, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"},
                {"id": 43, "time": datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"), "title": "test", "message": "message"}]

###
# Rate Limit
###

 
def get_real_ip():
    # X-Forwarded-For en prod (Apache), remote_addr en dev local
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr

limiter = Limiter(
    app=app,
    key_func=get_real_ip,
    default_limits=["10 per second"]
)


###
# Routes
###


@app.route("/")
def index():
    return render_template("html/index.html")
 
 
@app.route("/submit", methods=["POST"])
@limiter.limit("1 per minute")
def submit():
    global listMessages
    global messages_lock
    print(get_remote_address())
    data    = request.get_json(force=True, silent=True) or {}
    title   = str(data.get("title", "")).strip()[:300]
    message = str(data.get("message", "")).strip()[:5000]
 
    if not title:
        return {"ok": False, "error": "titre requis"}, 400
    if not message:
        return {"ok": False, "error": "message requis"}, 400
 
    with messages_lock:
        new_id = len(listMessages)
        listMessages.append({
            "id":      new_id,
            "time":    datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"),
            "title":   title,
            "message": message
        })

    return jsonify({"ok": True, "id": new_id})
 
@app.route("/messages")
def messages():
    if not session.get("logged"):
        return redirect(url_for("login"))
    return render_template("html/messages.html", twitch_username=TWITCH_USERNAME, website_domain=WEBSITE_DOMAIN)
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            with limiter.limit("1 per second"):
            # something expensive
                if request.form.get("password") == LOGIN_PASSWORD:
                    session["logged"] = True
                    return redirect(url_for("messages"))
                return render_template("html/login.html", error="Mot de passe incorrect.")
        except RateLimitExceeded:
            return render_template("html/login.html", error="Cooldown / Veuillez réessayer dans quelques secondes."), 429
    return render_template("html/login.html", error=None)
 
 
@app.route("/logout")
def logout():
    # Pop session logged
    session.pop("logged", None)
    return redirect(url_for("login"))
 
 
@app.route("/poll")
def poll():
    # If not logged => Not access
    if not session.get("logged"):
        return {}, 403
    # Parameter
    page = int(request.args.get("page", 1))
    maxMessages = int(request.args.get("maxMessages", 10))
    # Verify Parameter
    pagesNumber = math.ceil(len(listMessages)/maxMessages)
    page = pagesNumber if (page > pagesNumber) else page
    # Computing id values
    startingId = (page-1) * maxMessages
    endingId = (page * maxMessages) # Not included, so minus id-1 on JSON
    # JSON return
    return {"messages": listMessages[startingId:endingId], "pagesNumber": pagesNumber, "total": len(listMessages)}

###
# Main Script
###
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, threaded=True)
 