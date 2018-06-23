import spotify_config

print("Enter the artist name")
artist = input()

print("Enter the album name you want to dl")
album = input()

print(artist, album, spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)