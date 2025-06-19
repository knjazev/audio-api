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

        print("⬇️ Downloading audio with yt-dlp...")
        yt = subprocess.run([
            "yt-dlp",
            "--no-playlist",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", mp3_path,
            url
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("📄 yt-dlp stdout:\n", yt.stdout)
        print("⚠️ yt-dlp stderr:\n", yt.stderr)

        if yt.returncode != 0 or not os.path.exists(mp3_path):
            return jsonify({"error": "yt-dlp failed", "stderr": yt.stderr}), 500

        print("🎛 Converting to WAV with ffmpeg...")
        ff = subprocess.run([
            "ffmpeg", "-y", "-i", mp3_path, wav_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("📄 ffmpeg stdout:\n", ff.stdout)
        print("⚠️ ffmpeg stderr:\n", ff.stderr)

        if ff.returncode != 0 or not os.path.exists(wav_path):
            return jsonify({"error": "ffmpeg failed", "stderr": ff.stderr}), 500

        print("✅ Sending file")
        return send_file(wav_path, mimetype="audio/wav")

    except subprocess.CalledProcessError as e:
        print("❌ Subprocess error:", e)
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
    except Exception as e:
        print("❗️General error:", e)
        return jsonify({"error": str(e)}), 500