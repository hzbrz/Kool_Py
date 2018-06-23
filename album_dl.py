from __future__ import unicode_literals
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_config, spotipy, os, requests, bs4, youtube_dl, re

print("Enter the artist name")
artist = input()

name_split = artist.split(' ')
res_artist = ''
if len(name_split) > 1:
  res_artist = '+'.join(name_split)
else:
  res_artist = artist

print("Enter the album name you want to dl")
album_name = input()

# creating directory for downloaded songs
print('creating directory for album...')
dir = ''
try:
  dir = r'C:\Users\wazih\Desktop\songs\%s' %(album_name)
  os.makedirs(dir)
except WindowsError:
  print('dir already exists')
  dir = r'C:\Users\wazih\Desktop\songs\%s' %(album_name)

client_credentials_manager = SpotifyClientCredentials(
    spotify_config.spotify_client_ID, spotify_config.spotify_client_SECRET)
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

track_names = []
for album in albums['items']:
  # matching album name for downlaod
  if album['name'].lower() == album_name:
    tracks = sp.album_tracks(album['uri'])
    # list comprehens to generate an array with the track names
    track_names = [track['name'] for track in tracks['items']]

print('tracks:', track_names)

print('getting links from YT')
links = []
for track in track_names:
  # getting the url from youtube
  res = requests.get('https://www.youtube.com/results?search_query=' + res_artist + track)
  soup = bs4.BeautifulSoup(res.text, "html.parser")
  # selecting the specific tag to get the link
  vid_id = soup.select('h3 > a')
  link = 'https://www.youtube.com'+vid_id[0].get('href')  
  links.append(link)

print(links)

# downloading the videos
os.chdir(dir)
ydl_opts = {'format': 'bestaudio/best'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
  ydl.download(links)

# regex to get the song name before the extension
name_regex =  re.compile(r'^.*(?=(\.))')
# turning files into mp3
for file in os.listdir(dir):
  mo = name_regex.search(file)
  os.rename(dir + '\\' + file, dir + '\\' + mo.group() + '.mp3')

print('turned files into mp3')