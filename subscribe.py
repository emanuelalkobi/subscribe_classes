#!/usr/bin/env python3

import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import datetime
import http.client as httplib

URL_GRAND_KENYON_HAIFA="https://www.holmesplace.co.il/place-studio/?club=202"
CLASS="ספינינג"
PREF_SEATS =[39, 36, 35, 38, 27]
DATE=datetime.now()
LOG_PATH="/tmp/subscribe_log_%s.txt"%DATE


def check_internet(url="www.google.com", timeout=3):
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        connection.close()  # connection closed
        return True
    except Exception as exep:
        log(exep)
        return False

def log(text):
    text_file = open(LOG_PATH, "a")
    text_file.write("%s\n"%text)
    text_file.close()
    print(text)

def remove_add(driver):
    log("trying to remove advertise")
    try:
        close_ad = driver.find_element_by_class_name('close-icon')
        close_ad.click()
    except:
        log("Didn't find advertise")

#create an ArgumentParser object
parser = argparse.ArgumentParser(description = 'Subscribe to all Holmesplace classes')
#declare arguments
parser.add_argument('-n','--number', help='phone number to access account', required=True)
parser.add_argument('-p','--password', help='password to access account', required=True)
args = parser.parse_args()

log("Script starts to run at %s, subscribe to %s. Logs are located at %s"%(datetime.now(), CLASS, LOG_PATH)) 
if (not check_internet()):
    log("There is no internet connection, script can't run.")

options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized") 
options.add_argument('--log-level=3')

log("Creating Chrome driver")
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
driver.implicitly_wait(10)

log("Accessing %s"%URL_GRAND_KENYON_HAIFA)
driver.get(URL_GRAND_KENYON_HAIFA)

remove_add(driver)

log("Start login....")
access_login = driver.find_element(By.LINK_TEXT, "כניסה / הרשמה")
access_login.click()

remove_add(driver)

log("inserting password")
password = driver.find_element(By.ID, "LoginPassword")
password.clear()
password.send_keys(args.password)

log("inserting phone number")
phone = driver.find_element(By.ID, "LoginPhone")
phone.clear()
phone.send_keys(args.number)

remove_add(driver)

login = driver.find_element(By.ID, "loginButton")
login.click()

register = driver.find_elements_by_link_text('בחר מקום')
if not (len(register)):
    log("Error: Couldn't find any classes")

for class_idx,class_info in enumerate(register):
    try:
        class_str = class_info.get_attribute('outerHTML')
    except:
        continue
    class_name = class_str.partition("data-lessonname=\"")[2].split("\" ")[0]
    class_date = class_str.partition("data-date=\"")[2].split("\" ")[0]
    class_time = class_str.partition("data-time=\"")[2].split("\" ")[0]
    class_teacher = class_str.partition("data-teacher=\"")[2].split("\" ")[0]
    log("Class number %d name:%s date:%s time:%s teacher:%s"%(class_idx, class_name, class_date, class_time, class_teacher))
    
    if CLASS in class_info.get_attribute('outerHTML'):
        log(class_info.get_attribute('outerHTML'))
        sleep(10)
        class_info.click()
        seats= driver.find_element(By.ID, "availableSeatsSELECT")
        drop=Select(seats)
        pref_seat_choosen = False
        for pref_seat in PREF_SEATS:
            try:
                drop.select_by_visible_text(str(pref_seat))
                pref_seat_choosen = True
                print("Prefered seat %d was choosed"%pref_seat)
                break
            except:
                log("Seat %d is not available"%pref_seat)
        if not pref_seat_choosen:
            log("A default seat was choosen")
        register = driver.find_element_by_link_text('הזמנה')
        register.click()
        log("registered successfully to the class")

log("Close Chrome driver")
driver.close()
