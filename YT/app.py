from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "/tmp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            return "URL inválida"

        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': filepath,
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(filepath, as_attachment=True)

        except Exception as e:
            return f"Erro: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
