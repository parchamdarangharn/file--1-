from flask import Flask, request, send_from_directory
import  os 

app = Flask(__name__, static_folder=".", static_url_path="")

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "videos"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/login", methods=["GET"])
def login_page():
    return send_from_directory(".", "login.html")

@app.route("/")
def home():
    return "سایت با موفقیت اجرا شد!"


@app.route("/upload", methods=["POST"])
def upload_video():

    if "video" not in request.files:
        return "ویدیویی انتخاب نشده!"

    video = request.files["video"]

    if video.filename == "":
        return "ویدیویی انتخاب نشده!"

    print("FILE:", video)
    print("FILENAME:", video.filename)
    print("FOLDER:", app.config["UPLOAD_FOLDER"])

    try:
        video.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                video.filename
            )
        )

        print("SAVED!")
        return "ویدیو با موفقیت آپلود شد!"

    except Exception as e:
        print("SAVE ERROR:", e)
        return f"خطا در ذخیره فایل: {e}"


if __name__ == "__main__":
    app.run(debug=True)