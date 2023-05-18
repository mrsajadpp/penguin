import pafy
from youtubesearchpython import VideosSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests

client_id = 'ae048057336e4a1b9df086e9bd17112d'
client_secret = 'ec448ae380df4737a6abcd3efc4c223d'
# https://open.spotify.com/track/73virUhdH3B8pi53zaG2BL?si=76b680a6833e4852

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.track(track_id='73virUhdH3B8pi53zaG2BL')


def sp_download(track_url):
    payload = {
        'track_url': track_url
    }
    response = requests.post('http://localhost:3000/download', json=payload)
    if response.status_code == 200:
        data = response.json()
        return { 'file_path': data['song'], 'song_name': data['name'] }
