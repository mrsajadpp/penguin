from pytube import YouTube
import os
current_directory = os.getcwd()
from moviepy.editor import *
 
#https://youtu.be/DlIYupicuqM

# Create a YouTube object with the video URL
def yt_download(video_url,file_type):
  youtube = YouTube(video_url)
  # Get the highest resolution stream available
  stream = youtube.streams.get_highest_resolution()
  file_path = stream.download('src/', stream.default_filename)
  print(file_path)
  if(file_type == 'mp4'):
    return { "file_path": file_path, "stream": stream, "type": 'mp4' }
  else:
    video = VideoFileClip(file_path)
    video.audio.write_audiofile(file_path + '.mp3')
    return { "file_path": file_path + '.mp3', "stream": stream, "type": 'mp3' }