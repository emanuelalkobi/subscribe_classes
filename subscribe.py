#!/usr/bin/env python3

import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import datetime

URL_GRAND_KENYON_HAIFA="https://www.holmesplace.co.il/place-studio/?club=202"
CLASS="פילאטיס"
PREF_SEATS =[39, 36, 35, 38, 27]

def remove_add(driver):
    print("trying to remove advertise")
    try:
        close_ad = driver.find_element_by_class_name('close-icon')
        close_ad.click()
    except:
        print("Didn't find advertise")


#create an ArgumentParser object
parser = argparse.ArgumentParser(description = 'Subscribe to all Holmesplace classes')
#declare arguments
parser.add_argument('-n','--number', help='phone number to access account', required=True)
parser.add_argument('-p','--password', help='password to access account', required=True)
args = parser.parse_args()


print("Script starts to run at %s, subscribe to %s"%(datetime.now(), CLASS)) 
options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized") 
options.add_argument('--log-level=3')


print("Creating Chrome driver")
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)

print("Accessing %s"%URL_GRAND_KENYON_HAIFA)
driver.get(URL_GRAND_KENYON_HAIFA)


sleep(10)

remove_add(driver)

print("Start login....")
access_login = driver.find_element(By.LINK_TEXT, "כניסה / הרשמה")
access_login.click()

remove_add(driver)

sleep(5)

print("inserting password")
password = driver.find_element(By.ID, "LoginPassword")
password.clear()
password.send_keys(args.password)

print("inserting phone number")
phone = driver.find_element(By.ID, "LoginPhone")
phone.clear()
phone.send_keys(args.number)

sleep(5)

remove_add(driver)

login = driver.find_element(By.ID, "loginButton")
login.click()

sleep(10)

register = driver.find_elements_by_link_text('בחר מקום')
if not (len(register)):
    print("Error: Couldn't find any classes")

for class_idx,class_info in enumerate(register):
    try:
        class_str = class_info.get_attribute('outerHTML')
    except:
        continue
    class_name = class_str.partition("data-lessonname=\"")[2].split("\" ")[0]
    class_date = class_str.partition("data-date=\"")[2].split("\" ")[0]
    class_teacher = class_str.partition("data-teacher=\"")[2].split("\" ")[0]
    print("Class number %d name:%s date:%s teacher:%s"%(class_idx, class_name, class_date, class_teacher))
    
    #if "ספינינג" in class_info.get_attribute('outerHTML'):
        
    if CLASS in class_info.get_attribute('outerHTML'):
        print(class_info.get_attribute('outerHTML'))
        sleep(5)
        print("here -2")
        class_info.click()
        sleep(5)
        print("here -1")
        seats= driver.find_element(By.ID, "availableSeatsSELECT")
        sleep(5)
        print("here 0")
        drop=Select(seats)
        pref_seat_choosen = False
        for pref_seat in PREF_SEATS:
            try:
                drop.select_by_visible_text(str(pref_seat))
                pref_seat_choosen = True   
            except:
                print("Seat %d is not available"%pref_seat)
        if not pref_seat_choosen:
            print("A default seat was choosen")
        sleep(10)
        print("here1")
        register = driver.find_element_by_link_text('הזמנה')
        sleep(5)
        register.click()
        print("registered successfullyo to the class")
        print("here2")
        sleep(5)
        break


