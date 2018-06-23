from spotipy.oauth2 import SpotifyClientCredentials
import spotify_config, spotipy

print("Enter the artist name")
artist = input()

print("Enter the album name you want to dl")
album = input()

client_credentials_manager = SpotifyClientCredentials(spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
