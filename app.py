from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import show_error, login_required
from db.db import Database
from os import getcwd


app = Flask(__name__)
cwd = getcwd()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/video")
@login_required
def video():
    return render_template("video.html")

@app.route("/history")
@login_required
def history():
    return render_template("history.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return show_error("Invalid username")
        if not password:
            return show_error("Missing password")

        db = Database(cwd)
        user = db.fetchuser_byname(username)        
        if user is None:
            return show_error("User not found")
        elif not check_password_hash(user[2], password):
            return show_error("Invalid username or password")
        
        session["user_id"] = user[0]
        session["user_name"] = user[1]

        return redirect("index")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return show_error("Invalid username")
        if not password:
            return show_error("Missing password")
        if not confirmation:
            return show_error("Missing confirmation of password")
        if confirmation != password:
            return show_error("Passwords do not match")
        
        hash = generate_password_hash(password)

        db = Database(cwd)
        
        user = db.fetchuser_byname(username)
        if not user is None and user[1] == username:
            db.close()
            return show_error("Username alredy taken")
        else:
            db.register_user(username, hash)
            user = db.fetchuser_byname(username)
            db.close()
        
        session["user_id"] = user[0]
        session["user_name"] = user[1]

        return redirect("index")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("index")


if __name__ == "__main__":
    app.run()