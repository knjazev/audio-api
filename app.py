from flask import Flask, request, send_file
import subprocess, os, uuid

app = Flask(__name__)  # ← ОБЯЗАТЕЛЬНО до любых @app.route
@app.route("/extract", methods=["POST"])

def extract():
    try:
        print("📥 /extract called")
        data = request.json
        url = data.get("url")
        print(f"🔗 URL = {url}")

        if not url:
            return {"error": "No URL"}, 400

        uid = str(uuid.uuid4())
        mp3 = f"/tmp/{uid}.mp3"
        wav = f"/tmp/{uid}.wav"

        print("🔧 Step 1: Downloading mp3")
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", url, "-o", mp3], check=True)

        print("🔧 Step 2: Converting to wav")
        subprocess.run(["ffmpeg", "-i", mp3, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav, "-y"], check=True)

        print("✅ Sending file")
        return send_file(wav, mimetype="audio/wav")

    except Exception as e:
        print(f"❌ ERROR in /extract: {e}")
        return {"error": str(e)}, 500

    finally:
        for f in [mp3, wav]:
            if os.path.exists(f):
                os.remove(f)