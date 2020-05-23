from selenium import webdriver
import pymongo
import json
from bson import ObjectId
from carb_scraper import carbManagerStats

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["calendarDB"]

calorie_coll = mydb["calories"]
user_coll = mydb["users"]


users = user_coll.find()
if users.count() == 0:
  print("No users exist")
else:
  path = "C:\\Users\\wazih\\Desktop\\PFE\\api_projects\\carb-api"
  with open(path+"\\passwords.json", 'r') as infile:
    file_data = infile.read()
    json_data = json.loads(file_data)

  for user in users:
    # counter for how many times to check for the UI error
    count = 0
    # resetting data per user otherwise the while loop doesnt run and wrong data gets entered
    mydata = {'name': 'Total', 'carb': '--', 'fat': '--', 'protein': '--', 'calories': '--'}

    calorie_id = ObjectId(user["calorie_id"])
    # dealing with the carb manager UI error where the data does not show, thus I get empty data
    # so as long as it comes empty I will keep running the scraper over and over until I get data for 6 times
    # I keep count becasue on the days I do not log it doesnt scrape forever for some data
    while(count < 11 and mydata["calories"] == "--"):
      # try block for catchign accounts that are not carb manager accounts
      try:
        driver = webdriver.Chrome()
        mydata = carbManagerStats(user["email"], json_data[user["email"]], driver)
        driver.close()
        print(mydata)
      except:
        count = count + 6
        driver.close()
        print(mydata)

      count = count + 1

    if mydata["calories"] == "--":
      print("USER CANNOT LOG INTO CARBMANAGER")
    else:
      calorie_query = {"_id": calorie_id}
      calorie = calorie_coll.find(calorie_query)
      if calorie.count() == 0:
        print("Calorie calendar not found")

      for c in calorie:
        month1 = list(c.keys())[1]
        month2 = list(c.keys())[2]
        month3 = list(c.keys())[3]

        month1_dict = c[ list(c.keys())[1] ]
        month2_dict = c[ list(c.keys())[2] ]
        month3_dict = c[ list(c.keys())[3] ]
        
        # checking if the first month has any days
        if not month1_dict:
          print("No items")
          month1_dict["0"] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month1: month1_dict} }
          )
        # if the first month does have any days and they are less than 29 
        elif month1_dict and int(list(month1_dict.keys())[len(list(month1_dict.keys()))-1]) < 29:
          days = list(month1_dict.keys())
          last_day = int(days[len(days)-1])
        
          month1_dict[str(last_day+1)] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month1: month1_dict} }
          )
        # now checking if the second month has no days and the first month is full with 29 days
        elif not month2_dict and int(list(month1_dict.keys())[len(list(month1_dict.keys()))-1]) >= 29:
          days = list(month1_dict.keys())
          last_day = int(days[len(days)-1])

          month2_dict["0"] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month2: month2_dict} }
          )
        # if the second month does have any days and they are less than 29 
        elif month2_dict and int(list(month2_dict.keys())[len(list(month2_dict.keys()))-1]) < 29:
          days = list(month2_dict.keys())
          last_day = int(days[len(days)-1])
        
          month2_dict[str(last_day+1)] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month2: month2_dict} }
          )
        # for the last month checking if the third month has no days and the second month is full with 29 days
        elif not month3_dict and int(list(month2_dict.keys())[len(list(month2_dict.keys()))-1]) >= 29:
          days = list(month2_dict.keys())
          last_day = int(days[len(days)-1])

          month3_dict["0"] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month3: month3_dict} }
          )
        elif month3_dict and int(list(month3_dict.keys())[len(list(month3_dict.keys()))-1]) < 29:
          days = list(month3_dict.keys())
          last_day = int(days[len(days)-1])
        
          month3_dict[str(last_day+1)] = mydata
          update = calorie_coll.find_one_and_update(
            {"_id": c["_id"]},
            {"$set": {month3: month3_dict} }
          )
        else:
          print("Goal days MAXED")