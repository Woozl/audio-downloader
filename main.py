from yt_dlp import YoutubeDL
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify({"hello": "world"})

if __name__ == '__main__':
    app.run(port=3000, debug=True)