from spotipy.oauth2 import SpotifyClientCredentials
import spotify_config, spotipy

print("Enter the artist name")
artist = input()

print("Enter the album name you want to dl")
album = input()

client_credentials_manager = SpotifyClientCredentials(spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_id(name):
  results = sp.search(q='artist:' + name, type='artist')
  items = results['artists']['items']
  if len(items) > 0:
      return items[0]['uri']
  else:
      return None

artist_id = get_artist_id(artist)

# getting albums from spotify for atist with artist id
albums = sp.artist_albums(artist_id, limit=30)

print(albums)
