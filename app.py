from flask import Flask, request, send_from_directory, redirect, url_for, session, render_template
import os

# مسیر اصلی پروژه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ساخت Flask
app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

# کلید Session
app.secret_key = "change-this-secret-key"

# پوشه ویدیوها
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

        # رمز آزمایشی مدیر
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

    # اگر مدیر وارد نشده باشد
    if not session.get("admin_logged_in"):
        return redirect(url_for("login_page"))

    return send_from_directory(BASE_DIR, "admin.html")


# =========================
# خروج مدیر
# =========================

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("login_page"))


# =========================
# آپلود ویدیو
# =========================

@app.route("/upload", methods=["POST"])
def upload_video():

    # فقط مدیر اجازه آپلود دارد
    if not session.get("admin_logged_in"):
        return redirect(url_for("login_page"))

    if "video" not in request.files:
        return "ویدیویی انتخاب نشده!"

    video = request.files["video"]

    if video.filename == "":
        return "ویدیویی انتخاب نشده!"

    # ذخیره ویدیو
    video_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        video.filename
    )

    video.save(video_path)

    return "ویدیو با موفقیت آپلود شد!"

@app.route("/videos")
def videos_page():

    video_files = os.listdir(app.config["UPLOAD_FOLDER"])

    return render_template(
        "videos.html",
        videos=video_files
    )
# =========================
# اجرای برنامه
# =========================

if __name__ == "__main__":
    app.run(debug=True)