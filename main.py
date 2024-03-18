from yt_dlp import YoutubeDL
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<h1>Hello From Index!</h1>
<img
    src="https://images.unsplash.com/photo-1710722960765-dcb3df7723a3?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    width="300px"
/>
'''

@app.route('/hello')
def hello():
    return jsonify({"hello": "world"})

if __name__ == '__main__':
    app.run(port=3000, debug=True)