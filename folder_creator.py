import os

def make_folder(name):  
  # creating directory for downloaded songs
  print('creating directory for album...')
  dir = ''
  try:  
    dir = "C:\\Users\\wazih\\Desktop\\Musci\\%s" %(name)
    os.makedirs(dir)
  except WindowsError:
    print('dir already exists')
    dir = "C:\\Users\\wazih\\Desktop\\Musci\\%s" %(name)

  return dir

def move_tracks(dir, track_name):
  for files in os.walk("C:\\Users\\wazih\\Downloads"):
    for file in files: 
      if track_name == file:
        print("match")


