import requests

with requests.Session() as s:
  url = "https://www.loseit.com/account/?source=loseit-nav"
  r = s.get(url)
  print(r.content)