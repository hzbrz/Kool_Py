# https://st2.fileurl.link/file/825529672950506/

import urllib.request

url = input("Enter link: ")
url_name = input("name for vid: ")
video = "C:\\Users\\wazih\\Desktop\\"+ url_name + ".mp4" 
urllib.request.urlretrieve(url,  video)