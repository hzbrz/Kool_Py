from song_tracker import get_playlist, get_playlist_tracks
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_config, spotipy, pprint, requests, pickle

client_credentials_manager = SpotifyClientCredentials(
    spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# generating a spotify token for the request header and getting tracks from playlist
token = client_credentials_manager.get_access_token()

headers = { 'Authorization': 'Bearer ' + token  }

read_file = open('songs.pkl', 'rb')
file_content = pickle.load(read_file)
read_file.close() 

id_dir = get_playlist()
id = id_dir[0]
tracks = requests.get("https://api.spotify.com/v1/playlists/" +id+ "/tracks", headers=headers).json()
names = []
# gets the track names of the playlist
for track in tracks['items']:
  pprint.pprint(track["track"]["albums   "])
  print("--------------------------------\n\n")
  # names.append(track["track"]["name"])    

print(names)

print("BEFORE")
print(file_content)
print(len(file_content))
print("\n\n")  
for name in names:
  if name in file_content:
    file_content.remove(name) 

print("AFTER")
print(file_content)
print(len(file_content))

write_file = open('songs.pkl', 'wb') 
pickle.dump(file_content, write_file)
write_file.close()
# # get_playlist_tracks(id)

