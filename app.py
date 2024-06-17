from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, send_file, url_for
from flask_session import Session
from db.db import Database
from os import getcwd, path
from helpers import show_error, login_required, check_video
import subprocess


app = Flask(__name__)
cwd = getcwd()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["UPLOAD_FOLDER"] = path.join(cwd, "video")

FFMPEG_LOCAL = "ffmpeg.exe" # ffmpeg name on video folder
FFMPEG_BINARY = path.join(app.config.get("UPLOAD_FOLDER"), FFMPEG_LOCAL)

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

@app.route("/video", methods=["GET", "POST"])
@login_required
def video():
    if request.method == "POST":
        if "initialvideo" not in request.files:
            return show_error("No initial video part on form")
        initial_video = request.files.get("initialvideo")
        if "secondvideo" not in request.files:
            return show_error("No second video part no form")
        second_video = request.files.get("secondvideo")

        if initial_video.filename == "":
            return show_error("Not selected initial video")
        if second_video.filename == "":
            return show_error("Not selected second video")
        
        if not check_video(initial_video.mimetype):
            return show_error("Not a video")
        if not check_video(second_video.mimetype):
            return show_error("Not a video")

        initial_video.save(path.join(app.config.get("UPLOAD_FOLDER"), secure_filename(initial_video.filename)))
        second_video.save(path.join(app.config.get("UPLOAD_FOLDER"), secure_filename(second_video.filename)))

        # Filelist to get video names
        filelist_name = "filelist.txt"
        with open(path.join(app.config.get("UPLOAD_FOLDER"), filelist_name), "w") as filelist:
            filelist.write(f"file '{secure_filename(initial_video.filename)}'\n")
            filelist.write(f"file '{secure_filename(second_video.filename)}'\n")

        outputfile_name = "output.mp4" # Output video name
        output_path = path.join(app.config.get("UPLOAD_FOLDER"), "out", outputfile_name) # Path to output video
        # Concat video
        subprocess.run([FFMPEG_BINARY, '-f', 'concat', '-safe', '0', '-i',
                    path.join(app.config.get("UPLOAD_FOLDER"), filelist_name), '-c', 'copy', '-y', output_path])

        return redirect("download")
        # TODO: Reformat the code to be more organized
    else:
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

@app.route("/download")
def download():
    output_file = "output.mp4"
    output_folder = "out"
    return send_file(path.join(app.config.get("UPLOAD_FOLDER"), output_folder, output_file), as_attachment=True)
    


if __name__ == "__main__":
    app.run()