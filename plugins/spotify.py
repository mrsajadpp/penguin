import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'ae048057336e4a1b9df086e9bd17112d'
client_secret = 'ec448ae380df4737a6abcd3efc4c223d'

# Step 1: Set up Spotify client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Step 2: Get an access token
token = client_credentials_manager.get_access_token()

def sp_download(track_url):
  # Step 3: Extract the track ID from the URL
  track_id = track_url.split('/')[-1].split('?')[0]

  # Step 4: Get the track information
  track_info = spotify.track(track_id)

  # Step 5: Get the preview URL or the external URL
  preview_url = track_info['preview_url']
  external_url = track_info['external_urls']['spotify']

  # Print the URLs
  print(track_info)
  print('Preview URL:', preview_url)
  print('External URL:', external_url)
