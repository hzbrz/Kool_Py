from selenium import webdriver
from carb_scraper import carbManagerStats


f = open("./cred.txt","r")
lines = f.readlines()
email_cred = lines[1]
password_cred = lines[0]
f.close()

driver = webdriver.Chrome()
mydata = carbManagerStats(email_cred, password_cred, driver)
print(mydata)
driver.close()