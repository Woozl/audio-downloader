from yt_dlp import YoutubeDL
from flask import Flask, request, send_file, jsonify, Response, after_this_request
from flask_cors import CORS
import tempfile
from copy import deepcopy
from os import path

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

DEFAULT_OPTIONS = {
    "format": "best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ],
    "outtmpl": "%(title)s.%(ext)s",
}


@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return error("Please provide a `url` query param"), 400

    tempdir = tempfile.TemporaryDirectory()
    tempdir_path = tempdir.name

    @after_this_request
    def cleanup_tempdir(response):
        tempdir.cleanup()
        return response

    options = deepcopy(DEFAULT_OPTIONS)
    options["paths"] = {"home": tempdir_path}

    with YoutubeDL(options) as downloader:
        downloader.download(url)
        info_dict = downloader.extract_info(url, download=False)
        filepath = downloader.prepare_filename(info_dict).replace("mp4", "mp3")
        print(path.basename(filepath))
        return send_file(filepath, as_attachment=True, download_name=path.basename(filepath))


def error(message: str) -> Response:
    return jsonify({"error": message})


if __name__ == "__main__":
    app.run(port=3000, debug=True)
