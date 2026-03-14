from flask import Flask, render_template, send_from_directory
import os
from wifi_scanner import scan_wifi

app = Flask(__name__)

# absolute path to intruder folder
INTRUDER_FOLDER = os.path.join(os.getcwd(), "intruders")


# serve intruder images
@app.route("/intruders/<path:filename>")
def intruder_files(filename):
    return send_from_directory(INTRUDER_FOLDER, filename)


# get latest intruder image
def get_latest_intruder():

    if not os.path.exists(INTRUDER_FOLDER):
        return None

    files = os.listdir(INTRUDER_FOLDER)

    if not files:
        return None

    latest = max(
        files,
        key=lambda x: os.path.getctime(os.path.join(INTRUDER_FOLDER, x))
    )

    return latest


@app.route("/")
def home():

    devices = scan_wifi()

    intruder_image = get_latest_intruder()

    return render_template(
        "dashboard.html",
        devices=devices,
        intruder_image=intruder_image
    )


if __name__ == "__main__":
    app.run(debug=True)