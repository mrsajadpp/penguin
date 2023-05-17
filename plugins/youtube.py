from pytube import YouTube

# Ask the user for the YouTube video URL
video_url = input("Enter the YouTube video URL: ")

# Create a YouTube object with the video URL
youtube = YouTube(video_url)

# Get the highest resolution stream available
stream = youtube.streams.get_highest_resolution()

# Get the default output filename
output_filename = stream.default_filename

# Download the video
print(f"Downloading video: {output_filename}")
stream.download()

print("Video downloaded successfully!")
