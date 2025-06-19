from flask import Flask, request, send_file
import subprocess, os, uuid

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    data = request.json
    url = data.get("url")
    if not url:
        return {"error": "No URL"}, 400

    uid = str(uuid.uuid4())
    mp3 = f"/tmp/{uid}.mp3"
    wav = f"/tmp/{uid}.wav"

    try:
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", url, "-o", mp3], check=True)
        subprocess.run(["ffmpeg", "-i", mp3, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav, "-y"], check=True)
        return send_file(wav, mimetype="audio/wav")
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        for f in [mp3, wav]:
            if os.path.exists(f): os.remove(f)

@app.route("/", methods=["GET"])
def index():
    return "✅ Audio API ready"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print("💡 Using PORT =", port)
    app.run(host="0.0.0.0", port=port)