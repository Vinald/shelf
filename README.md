# shelf

A local web app for reading your PDF and Markdown library in the browser.
It scans a folder on disk, lists everything in a searchable sidebar, and
renders PDFs and Markdown files without needing an account, a cloud
service, or any of your files leaving your machine.

## Features

- Browse and search your library from the sidebar
- Read PDFs with pagination and zoom, rendered client-side with PDF.js
- Read Markdown files, rendered to sanitized HTML
- Read Aloud: listen to the current book via the browser's built-in speech synthesis, auto-advancing page by page
- Open a file from anywhere on disk, not just the library folder (no upload — the browser reads it directly)
- Runs natively with Python or in Docker

## Project structure

```
shelf/
├── app.py                 FastAPI backend: lists and serves library files
├── templates/index.html   the entire frontend (UI, PDF.js, read-aloud, markdown rendering)
├── requirements.txt       Python dependencies
├── Dockerfile             container image definition
└── docker-compose.yml     mounts your library folder and runs the container
```

There's no database and no build step. The backend's only job is to list
files in a folder and stream them back; everything else (rendering,
search, read-aloud) happens in the browser.

## Setup

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## Run

```
./venv/bin/python app.py
```

Then open http://localhost:5000

## Configuration

The app reads these environment variables at startup (all optional):

| Variable    | Default        | Purpose                                  |
|-------------|----------------|-------------------------------------------|
| `BOOKS_DIR` | `~/Books`      | Folder scanned for `.pdf` and `.md` files |
| `HOST`      | `127.0.0.1`    | Interface to bind to                      |
| `PORT`      | `5000`         | Port to listen on                         |

You can also just edit `BOOKS_DIR` directly at the top of `app.py`.

## Docker

Build it yourself:

```
docker compose up --build
```

This mounts `~/Books` from the host into the container and serves the app
at http://localhost:5000. Edit the volume line in `docker-compose.yml` if
your library lives somewhere else.

Or pull the prebuilt image instead of building it:

```
docker pull ghcr.io/vinald/shelf:1.0
docker run -d -p 5000:5000 -v ~/Books:/books ghcr.io/vinald/shelf:1.0
```

## How it works

- `GET /books` scans `BOOKS_DIR` and returns each `.pdf`/`.md` file's name,
  title, and type as JSON.
- `GET /read/<name>` streams one file back, after checking it resolves to
  a plain filename inside `BOOKS_DIR` (no path traversal).
- The frontend fetches `/books` to populate the sidebar, then either feeds
  a PDF's URL to PDF.js or fetches and renders a Markdown file's raw text.
- "Open file from computer" bypasses the backend entirely: the browser's
  file picker hands PDF.js or the Markdown renderer the file's bytes
  directly, so you can read a file from anywhere without it ever touching
  `BOOKS_DIR` or the server.
