FROM python:3.10-slim

RUN apt update && \
    apt install -y ffmpeg curl && \
    pip install yt-dlp flask gunicorn

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD exec gunicorn -w 1 -b 0.0.0.0:${PORT} app:app