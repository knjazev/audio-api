FROM python:3.10-slim

RUN apt update &&     apt install -y ffmpeg curl &&     pip install yt-dlp flask

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
