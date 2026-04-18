# Import
import os
import secrets
import math
import threading
import zoneinfo
import json

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
SERVER_PORT     = os.getenv("SERVER_PORT", 5000)
DEVMODE         = os.getenv("DEVMODE", False)

app = Flask(__name__, template_folder="template", static_folder="static", static_url_path="/static")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
app.secret_key = SECRET_KEY
 
###
# Var
###
messages_lock = threading.Lock()
listMessages = []

# DEV AREA #
if(DEVMODE):
    with open("test/messageTest.json", "r") as f:
        listMessages = json.load(f)
# DEV AREA #
#  
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
    # Get form data
    data    = request.get_json(force=True, silent=True) or {}
    title   = str(data.get("title", "")).strip()[:300]
    message = str(data.get("message", "")).strip()[:5000]
    # If it's missing something, tell it
    if not title:
        return {"ok": False, "error": "titre requis"}, 400
    if not message:
        return {"ok": False, "error": "message requis"}, 400
    # Acquire lock to add the anecdote to list
    with messages_lock:
        new_id = len(listMessages)
        listMessages.append({
            "id":      new_id,
            "time":    datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%H:%M:%S"),
            "title":   title,
            "message": message,
            "seen": False
        })
    # Return 200 and the anecdote id to user
    return jsonify({"ok": True, "id": new_id})
 
@app.route("/messages/<messageId>", methods=["PATCH"])
def patchMessages(messageId):
    global listMessages
    global messages_lock

    # If not logged => Not access
    if not session.get("logged"):
        return {}, 403
    
    # Get data for request
    data    = request.get_json(force=True, silent=True) or {}
    seen   = str(data.get("seen", "")).strip()
    # Acquire lock to change the seen attribute of anecdote
    with messages_lock:
        listMessages[int(messageId)]["seen"] = True if (seen == "True") else False
    # Return a 200, not really checked in fact
    return jsonify({"ok": True})

@app.route("/messages", methods=["GET"])
def messages():
    # If not logged => Not access
    if not session.get("logged"):
        return redirect(url_for("login"))
    # Render the anecdote page
    return render_template("html/messages.html", twitch_username=TWITCH_USERNAME, website_domain=WEBSITE_DOMAIN)
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            # Just to make sure someone is not spamming to discover the password :)
            with limiter.limit("1 per second"):
                # Connect and go to anecdote page if the password is good
                if request.form.get("password") == LOGIN_PASSWORD: # TODO : Maybe should I hash it ? 
                    session["logged"] = True
                    return redirect(url_for("messages"))
                return render_template("html/login.html", error="Mot de passe incorrect.")
        except RateLimitExceeded: # Someone without the password is spamming and I'm seeing it in the logs eheh
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
    if(page == 0):
        page = 1
        pagesNumber = 1
    # Computing id values
    startingId = (page-1) * maxMessages
    endingId = (page * maxMessages) # Not included, so minus id-1 on JSON
    # JSON return
    return {"messages": listMessages[startingId:endingId], "pagesNumber": pagesNumber, "total": len(listMessages)}

###
# Main Script
###
if __name__ == "__main__":
    DEBUG_MODE = False
    HOST = "0.0.0.0"
    # DEV AREA #
    if(DEVMODE):
        DEBUG_MODE = True
        HOST = "127.0.0.1"
    # DEV AREA #
    # Launch Flask Server
    app.run(host=HOST, port=SERVER_PORT, debug=DEBUG_MODE, threaded=True)
 