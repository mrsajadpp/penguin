import shutil
from plugins.youtube import yt_download
from plugins.spotify import sp_download
from plugins.instagram import ig_download
import requests
from flask import Flask, render_template, request, send_file, Response, make_response
import io
import os
import time
from datetime import date

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

# Instagram download section


@app.route('/instagram')
def igdl():
    return render_template('instagram.html')


@app.route('/instagram/download', methods=["POST"])
def igtdl():
    reel_url = request.form.get('url')
    doc_type = request.form.get('type')
    response = ig_download(reel_url, doc_type)
    # Handle the downloaded stream as needed
    print(response['reel_url'])
    # Download the file from the external link
    res = requests.get(response['reel_url'])
    if (response['status'] == 200):
        if (response['type'] == 'mp4'):

            # Set the appropriate headers for the response
            headers = {
                'Content-Type': res.headers.get('Content-Type'),
                'Content-Disposition': 'attachment; filename="Instagram - ' + date.today().strftime('%Y-%m-%d') + '" - Penguin.mp4'
            }

            # Create a response object with the downloaded file content and headers
            file_response = make_response(res.content)
            file_response.headers = headers

            return file_response
        else:
            return send_file(res.content, download_name=response['file_name'] + '.mp3', as_attachment=True, mimetype='audio/mp3')
    else:
        return "There was an error"


def clean_directory():
    directory = "src/"
    current_time = time.time()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Get the time of last modification of the file
            file_time = os.path.getmtime(file_path)

            # Calculate the time difference in seconds
            time_difference = current_time - file_time

            # Convert 24 hours to seconds
            twenty_four_hours = 24 * 60 * 60

            if time_difference > twenty_four_hours:
                os.remove(file_path)
                print(f"Deleted file: {filename}")


# Call the clean_directory function
clean_directory()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
