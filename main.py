from yt_dlp import YoutubeDL
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from tempfile import TemporaryDirectory
from copy import deepcopy
from os import path, environ

app = FastAPI()

# If we're in development, allow CORS to let Vite dev server communicate.
# If we're in production, we don't need it as the static frontend is hosted
# by this server and all requests are same-origin
if environ.get("PYTHON_ENV") != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

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

@app.get("/download")
def download(url: str, background_tasks: BackgroundTasks):
    tempdir = TemporaryDirectory()

    # when this request is done, clean up the temporary directory and audio track
    background_tasks.add_task(cleanup_tempdir, tempdir)

    options = deepcopy(DEFAULT_OPTIONS)
    options["paths"] = {"home": tempdir.name}

    with YoutubeDL(options) as downloader:
        downloader.download(url)
        info_dict = downloader.extract_info(url, download=False)
        filepath = downloader.prepare_filename(info_dict).replace("mp4", "mp3")

        response = FileResponse(filepath, media_type="audio/mpeg")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={path.basename(filepath)}"
        )
        return response

# this env var is set in the production Dockerfile, which handles building the React
# frontend and placing the static files in the appropriate directory. For development,
# use the separate Vite dev server for hot module reloading.
if environ.get("PYTHON_ENV") == "production":
    app.mount("/", StaticFiles(directory="./frontend/dist", html=True), name="static")

def cleanup_tempdir(tempdir: TemporaryDirectory[str]) -> None:
    tempdir.cleanup()
