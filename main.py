import shutil
from plugins.youtube import download
from flask import Flask, render_template, request, send_file, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/youtube')
def yt():
    return render_template("youtube.html")

@app.route('/youtube/download', methods=["POST"])
def ytdl():
    video_url = request.form.get('url')
    file_type = request.form.get('type')
    response = download(video_url, file_type)
    # Handle the downloaded stream as needed
    if(response):
      return send_file(response['file_path'], download_name=response['stream'].default_filename, as_attachment=True, mimetype='video/mp4')
    return send_file(response['file_path'], download_name=response['stream'].default_filename, as_attachment=True, mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
