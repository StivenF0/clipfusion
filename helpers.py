from flask import render_template, session, redirect
from functools import wraps

def show_error(msg: str):
    return render_template("error.html", message=msg)

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapped

def check_video(mime: str):
    return mime.split("/")[0] == "video"