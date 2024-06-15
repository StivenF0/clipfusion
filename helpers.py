from flask import render_template

def show_error(msg: str):
    return render_template("error.html", message=msg)