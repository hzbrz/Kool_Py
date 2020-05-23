from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def carbManagerStats(email_cred, password_cred, driver):
  driver.get("https://app.carbmanager.com/account/signin")
  
  email = driver.find_element_by_name('email')
  password = driver.find_element_by_name('password')
  # button = driver.find_element_by_xpath("//button[@class='primary full-width']")

  email.send_keys(email_cred)
  print("Email entered")
  time.sleep(1)
  password.send_keys(password_cred, Keys.ENTER)
  print("Password entered \n Logging in....")

  total_row = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@class='bg-amber-3 meals-table-header']")))
  totals = total_row.text
  total_arr = totals.split(' ')
  name, carb, fat, protein, cals = tuple(total_arr)

  data = dict(
    name = name,
    carb = carb,
    fat = fat,
    protein = protein,
    calories = cals
  )

  return data


