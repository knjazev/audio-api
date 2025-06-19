FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp && \
    mkdir -p /app

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
