from flask import Flask, request, send_from_directory, redirect, url_for, session, render_template
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
app.secret_key = "change-this-secret-key"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "videos")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# صفحه اصلی
# =========================

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")
# =========================
# ورود مدیر
# =========================

@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":

        password = request.form.get("password")

        if password == "1234":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_page"))

        return "رمز عبور اشتباه است!"

    return send_from_directory(BASE_DIR, "login.html")


# =========================
# پنل مدیریت
# =========================

@app.route("/admin")
def admin_page():

    if not session.get("admin_logged_in"):
        return redirect(url_for("login_page"))

    return render_template(
    "admin.html",
    videos=[
        filename for filename in os.listdir(UPLOAD_FOLDER)
        if filename.lower().endswith(
            (".mp4", ".webm", ".ogg", ".mov", ".m4v")
        )
    ]
)


# =========================
# خروج
# =========================

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("login_page"))

# =========================
# حذف ویدیو
# =========================

@app.route("/delete/<filename>", methods=["POST"])
def delete_video(filename):

    if not session.get("admin_logged_in"):
        return redirect(url_for("login_page"))

    filename = secure_filename(filename)

    video_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(video_path):
        os.remove(video_path)

    return redirect(url_for("admin_page"))
# =========================
# آپلود ویدیو
# =========================

@app.route("/upload", methods=["POST"])
def upload_video():

    if not session.get("admin_logged_in"):
        return redirect(url_for("login_page"))

    if "video" not in request.files:
        return "ویدیویی انتخاب نشده!"

    video = request.files["video"]

    if video.filename == "":
        return "ویدیویی انتخاب نشده!"

    filename = secure_filename(video.filename)

    video_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    video.save(video_path)

    return redirect(url_for("videos_page"))


# =========================
# نمایش خودکار ویدیوها
# =========================

@app.route("/videos")
def videos_page():

    videos = []

    for filename in os.listdir(UPLOAD_FOLDER):

        if filename.lower().endswith(
            (".mp4", ".webm", ".ogg", ".mov", ".m4v")
        ):
            videos.append(filename)

    videos.sort()

    return render_template(
        "videos.html",
        videos=videos
    )


# =========================
# پخش فایل ویدیو
# =========================

@app.route("/videos/<filename>")
def video_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =========================
# اجرای برنامه
# =========================


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)