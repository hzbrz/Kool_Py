from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from song_tracker import get_playlist, get_playlist_tracks
from folder_creator import move_tracks
import time

print("Are you trying to download an album, Y/N:")
answer = input()

playlist_tracks = []
artists = []
playlist_dir = ""
if answer == 'Y':
  print("Album feature under WIP")
else:
  # getting the id and dir
  id_dir = get_playlist()
  id = id_dir[0]
  playlist_dir = id_dir[1]
  # getting the playlist tracks and artists arrays
  playlist_artist = get_playlist_tracks(id)
  playlist_tracks = playlist_artist[0]
  artists = playlist_artist[1]

print('\n', playlist_tracks)
print(artists)

# geckodriver not working as of 10/24 so using chromedriver
browser = webdriver.Chrome()
browser.get("https://www.mp3juices.cc/")

# the site's main search bar to find music
search = browser.find_element_by_id('query')

for i in range(len(playlist_tracks)):
  # getting only one name in the search query
  for track in playlist_tracks[i:i+1]:
    search.send_keys(Keys.CONTROL + 'a')
    search.send_keys(Keys.BACKSPACE)
    time.sleep(5)
    search.send_keys(artists[i] + " " + track, Keys.ENTER)
    try:
      first_title_button = WebDriverWait(browser, 5).until(
                           EC.presence_of_element_located((By.XPATH, "//div[@id='result_1']/div[@class='options']/a[1]")))
      first_title_button.click()
    except:
      print("No results found")

    try:
      dl_button = WebDriverWait(browser, 15).until(
                  EC.element_to_be_clickable((By.XPATH, "//div[@id='download_1']/div[@class='options']/a[1]")))
      dl_button.click()
    except:
      try:
        dl_button = WebDriverWait(browser, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@id='download_1']/div[@class='options']/a[1]")))
        dl_button.click()
      except:
        print("result not found")      
      # print("result not found AGAIN!")

    # move_tracks(playlist_dir, track)


    time.sleep(5)

browser.close()