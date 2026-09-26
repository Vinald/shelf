# pdf-reader

A local web app for reading your PDF and Markdown library in the browser.

## Features

- Browse and search your library from the sidebar
- Read PDFs with pagination and zoom, rendered client-side with PDF.js
- Read Markdown files rendered to HTML
- Read Aloud: listen to the current book via the browser's speech synthesis
- Open a file from anywhere on disk, not just the library folder

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

## Library folder

By default the app looks for `.pdf` and `.md` files in `~/Books`. Change
`BOOKS_DIR` at the top of `app.py` to point somewhere else.
