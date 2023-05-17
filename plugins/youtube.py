from pytube import YouTube
import os
current_directory = os.getcwd()
os.environ["IMAGEIO_FFMPEG_EXE"] = current_directory + "/ffmpeg/bin/ffmpeg"
from moviepy.editor import *

print("YouTube plugin is up.")

#https://youtu.be/DlIYupicuqM

# Create a YouTube object with the video URL
def download(video_url,file_type):
  youtube = YouTube(video_url)
  # Get the highest resolution stream available
  stream = youtube.streams.get_highest_resolution()
  file_path = stream.download()
  if(file_type == 'mp4'):
    return { "file_path": file_path, "stream": stream }
  video = VideoFileClip(file_path)
  video.audio.write_audiofile("example.mp3")

  return False