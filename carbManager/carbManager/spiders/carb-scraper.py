import scrapy
from loginform import fill_login_form
import requests

f=open("../cred.txt","r")
lines=f.readlines()
password=lines[0]
f.close()


class LoseItLogin(scrapy.Spider):
  name = 'LoseItspider'

  start_urls = [
      'https://www.loseit.com/'
  ]

  login_url = 'https://www.loseit.com/account/?source=loseit-nav'

  login_user = 'wazihsabir@gmail.com'
  login_password = password

  def start_requests(self):
    # let's start by sending a first request to login page
    yield scrapy.Request(self.login_url, self.parse_login)

  def parse_login(self, response):
    # got the login page, let's fill the login form...
    data, url, method = fill_login_form(response.url, response.body,
                                        self.login_user, self.login_password)
    print("\n\n\n", data, url, method)

    # ... and send a request with our login data
    return scrapy.FormRequest(url, formdata=dict(data), method=method, callback=self.start_crawl)

  def start_crawl(self, response):
    print("HELOOOOOOOOOOOOOOOOOOOOOOOOOOOOoo")
    # OK, we're in, let's start crawling the protected pages
    for url in self.start_urls:
      yield scrapy.Request(url, callback=self.after_login)
      print(url)

  def after_login(self, response):
    print("\n\n\n HELOOOOOOOOOOOOOO", response)
    # nav = response.xpath('//*').get()
    # self.logger.info(nav)
    
  def parse(self, response):
      # do stuff with the logged in response
      self.logger.info("I think I am logged in")
      # all = response.xpath('//*').get()
      # nav = response.xpath('//div[@GKND-T5BEOC]').get()
      # self.logger.info(nav)
      # self.logger.info(all)
