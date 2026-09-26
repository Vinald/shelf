import os

from flask import Flask, abort, jsonify, render_template, send_file

app = Flask(__name__)

BOOKS_DIR = os.path.expanduser("~/Books")

EXTENSIONS = {".pdf": "pdf", ".md": "md"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/books")
def books():
    if not os.path.isdir(BOOKS_DIR):
        return jsonify([])

    result = []
    for f in os.listdir(BOOKS_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in EXTENSIONS:
            result.append({"name": f, "title": f[: -len(ext)], "type": EXTENSIONS[ext]})

    result.sort(key=lambda b: b["title"].lower())
    return jsonify(result)


@app.route("/read/<path:name>")
def read(name):
    ext = os.path.splitext(name)[1].lower()
    if os.path.basename(name) != name or ext not in EXTENSIONS:
        abort(404)

    path = os.path.join(BOOKS_DIR, name)
    if not os.path.isfile(path):
        abort(404)

    mimetype = "application/pdf" if ext == ".pdf" else "text/markdown"
    return send_file(path, mimetype=mimetype)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
