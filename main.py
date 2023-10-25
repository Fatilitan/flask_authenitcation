import os
from flask import Flask, redirect, render_template, request, session, url_for
from helpers import get_users, hash_password

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/home")
def redirect_index():
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", title="Index")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/lon")
def lon():
    return render_template("lon.html", title="League of Nations")


@app.route("/login", methods=["GET", "POST"])
def login():
    render_template("login.html", title="Login")
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        password = request.form["password"]
        session["password"] = password
        password_hash = hash_password(password)
        if password_hash == get_users().get(username):
            return redirect(url_for("dashboard"))
        return render_template("login.html", title="Login", error=True)
    elif request.method == "GET":
        return render_template("login.html", title="Login", error=False)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" in session and session["user"]:
        return render_template(
            "dashboard.html", title="Dashboard", loggedIn=True, name=session["user"]
        )
    else:
        return render_template("dashboard.html", title="Dashboard", loggedIn=False)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))
