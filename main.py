import shutil
from plugins.youtube import yt_download
from plugins.spotify import sp_download
from flask import Flask, render_template, request, send_file, Response, make_response
import io

app = Flask(__name__)

# Home page


@app.route('/')
def home():
    return render_template("home.html")

# YouTube downlosder section


@app.route('/youtube')
def yt():
    return render_template("youtube.html")


@app.route('/youtube/download', methods=["POST"])
def ytdl():
    video_url = request.form.get('url')
    file_type = request.form.get('type')
    response = yt_download(video_url, file_type)
    # Handle the downloaded stream as needed
    if (response['type'] == 'mp4'):
        return send_file(response['file_path'], download_name=response['stream'].default_filename, as_attachment=True, mimetype='video/mp4')
    else:
        print(response['file_path'])
        return send_file(response['file_path'], download_name=response['stream'].default_filename, as_attachment=True, mimetype='audio/mp3')

# Spotify downloader section


@app.route('/spotify')
def spdl():
    return render_template("spotify.html")


@app.route('/spotify/download', methods=["POST"])
def sptdl():
    track_url = request.form.get('url')
    response = sp_download(track_url)
    print(response['file_path'])
    return send_file(response['file_path'], download_name=response['song_name'] + '.mp3', as_attachment=True, mimetype='audio/mp3')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
