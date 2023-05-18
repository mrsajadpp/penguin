import requests

# Call the function with the URL of the Instagram reel

def ig_download(reel_url, doc_type):
    payload = {
        'reel_url': reel_url
    }
    response = requests.post('http://localhost:3000/ig/download', json=payload)
    if(doc_type == 'mp4'):
      if response.status_code == 200:
          data = response.json()
          if(data['status'] == 200):
            return { 'reel_url': data['video_url'], 'file_name': data['name'], 'type': 'mp4', 'status': 200 } 
          else:
            return { 'type': 'mp4', 'status': 404 }