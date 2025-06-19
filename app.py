from flask import Flask, request, send_file, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    print("📥 /extract endpoint hit")
    try:
        url = request.json.get("url")
        print("🔗 Got URL:", url)
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        uid = str(uuid.uuid4())
        mp3_path = f"/tmp/{uid}.mp3"
        wav_path = f"/tmp/{uid}.wav"

        print("⬇️ Downloading audio...")
        subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", mp3_path, url], check=True)

        print("🎛 Converting to WAV...")
        subprocess.run(["ffmpeg", "-y", "-i", mp3_path, wav_path], check=True)

        print("✅ Sending file")
        return send_file(wav_path, mimetype="audio/wav")

    except subprocess.CalledProcessError as e:
        print("❌ Subprocess error:", e)
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
    except Exception as e:
        print("❗️General error:", e)
        return jsonify({"error": str(e)}), 500