import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.expanduser("~/Books")

EXTENSIONS = {".pdf": "pdf", ".md": "md"}


@app.get("/", response_class=HTMLResponse)
def index():
    with open(os.path.join(BASE_DIR, "templates", "index.html")) as f:
        return f.read()


@app.get("/books")
def books():
    if not os.path.isdir(BOOKS_DIR):
        return []

    result = []
    for f in os.listdir(BOOKS_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in EXTENSIONS:
            result.append({"name": f, "title": f[: -len(ext)], "type": EXTENSIONS[ext]})

    result.sort(key=lambda b: b["title"].lower())
    return result


@app.get("/read/{name:path}")
def read(name: str):
    ext = os.path.splitext(name)[1].lower()
    if os.path.basename(name) != name or ext not in EXTENSIONS:
        raise HTTPException(status_code=404)

    path = os.path.join(BOOKS_DIR, name)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404)

    mimetype = "application/pdf" if ext == ".pdf" else "text/markdown"
    return FileResponse(path, media_type=mimetype)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
