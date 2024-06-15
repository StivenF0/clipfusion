from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()