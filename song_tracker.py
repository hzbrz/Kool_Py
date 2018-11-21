from spotipy.oauth2 import SpotifyClientCredentials
from folder_creator import make_folder
import spotify_config, spotipy, pprint, requests, pickle, os

# initialize and create file for tracking songs 
# create_file = open('songs.pkl', 'wb')
# pickle.dump([], create_file)
# create_file.close()

client_credentials_manager = SpotifyClientCredentials(
    spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# generating a spotify token for the request header and getting tracks from playlist
token = client_credentials_manager.get_access_token()

headers = { 'Authorization': 'Bearer ' + token  }

def get_playlist():
  return_arr = []
  print("Choose a category:\n")
  categories = sp.categories()
  print("name    id")
  print("---------------------")
  for category in categories["categories"]["items"]:
    print(category["name"] + "---" + category["id"])
  
  chosen_cat = input()

  name_index = []
  print("\nHere are the playlists from that category:")
  # use the playlist name to get the playlist id and then get the tracks from there
  playlists = sp.category_playlists(category_id=chosen_cat)
  for playlist in playlists["playlists"]["items"]:
    print(playlist["name"], playlist["tracks"]["total"])
    name_index.append(playlist["name"].lower())

  # print(name_index)
  print("\nchose a playlist name:")
  chosen_playlist = input()
  # making and catching the directory for the playlist
  directory = make_folder(chosen_playlist)

  playlist_id = playlists["playlists"]["items"][name_index.index(chosen_playlist)]["id"]
  
  # returning multiple things in a 2 dim arr, the id and the directory for moving files
  return_arr.append(playlist_id)
  return_arr.append(directory)

  return return_arr

def get_playlist_tracks(id):
  # counter for numbering and debugging
  counter = 0

  read_file = open('songs.pkl', 'rb')
  file_content = pickle.load(read_file)
  read_file.close() 

  # request to get the playlist's tracks using the playlists id
  # curl -X GET "https://api.spotify.com/v1/playlists/{playlist id}/tracks" -H "Authorization: Bearer {token}"
  tracks = requests.get("https://api.spotify.com/v1/playlists/" +id+ "/tracks", headers=headers).json()

  playlist_artist_arr = []
  playlist_tracks = []
  artists = []
  # gets the track names of the playlist
  for track in tracks['items']:
    print(counter, track['track']['name'])

    # checking if the song exists in the file
    if track['track']['name'] in file_content:
      print("song already in playlist")
    else:
      playlist_tracks.append(track['track']['name'])
      file_content = file_content + [ track['track']['name'] ]
      artists.append(track['track']['artists'][0]['name'])
    counter = counter + 1

  print('\n', file_content)
  write_file = open('songs.pkl', 'wb') 
  pickle.dump(file_content, write_file)
  write_file.close()
  
  # creating the two dim array because this func needs to return two arrays, the arrays are inside the 2dim arr
  playlist_artist_arr.append(playlist_tracks)
  playlist_artist_arr.append(artists)

  # debugging
  print('\n', playlist_tracks, len(playlist_tracks))
  print('\n', artists, len(artists))
  print('\n', playlist_artist_arr)

  return playlist_artist_arr
