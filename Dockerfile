FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

ENV HOST=0.0.0.0
ENV BOOKS_DIR=/books

EXPOSE 5000

CMD ["python", "app.py"]
