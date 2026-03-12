from flask import Flask, render_template
from wifi_scanner import scan_wifi

app = Flask(__name__)


@app.route("/")
def home():

    devices = scan_wifi()

    return render_template("dashboard.html", devices=devices)


if __name__ == "__main__":
    app.run(debug=True)