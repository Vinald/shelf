import os

from flask import Flask, abort, jsonify, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

BOOKS_DIR = os.path.expanduser("~/Books")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/books")
def books():
    if not os.path.isdir(BOOKS_DIR):
        return jsonify([])

    pdfs = [f for f in os.listdir(BOOKS_DIR) if f.lower().endswith(".pdf")]
    result = [{"name": f, "title": f[:-4]} for f in pdfs]
    result.sort(key=lambda b: b["title"].lower())
    return jsonify(result)


@app.route("/read/<path:name>")
def read(name):
    safe_name = secure_filename(name)
    path = os.path.join(BOOKS_DIR, safe_name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
