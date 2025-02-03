# Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from urllib.request import urlopen
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

import psycopg2
import psycopg2.extras

import sys

import json

import logging

import requests
from requests.structures import CaseInsensitiveDict

import os

import time
import datetime

from selectolax.parser import HTMLParser
import concurrent.futures

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

import random

def addPic(link):
    id = random.randint(1, 10)

    picPath = 'images/' + str(id) + '.jpg'

    urlretrieve(link, picPath)

    print(picPath)

'''
# Remove photos - may change to non-looped depending on where its used
def removePic(picture_id):
    """
    for pic in picture_ids:
        picPath = startPath + str(pic) + ".jpg"
        os.remove(picPath)
    """
    
    picPath = startPath + str(picture_id) + ".jpg"
    #os.remove(picPath)

    if os.path.exists(picPath):
        os.remove(picPath)
    else:
        print("The file: " + picPath + " does not exist")
'''

def getOnlineStuff():
    # Regular search:
    """
    options = ChromeOptions()
    #options.browser_version = '114' #need to get updated to main version
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    """
    #Set up Chrome options for headless mode
    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass the sandbox (needed for Docker)
    options.add_argument("--disable-dev-shm-usage")  # Overcome Docker’s memory limitations
    options.add_argument("--disable-notifications")

    options.browser_version = '114' # says that the chrome driver only supports version 114

    # Initialize the WebDriver with the configured options
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)

    driver.get("https://www.google.com/")

    time.sleep(5)

    print(driver.title)

link = "https://images.all-free-download.com/images/thumbjpg/test_testing_optical_265619.jpg"

addPic(link)

getOnlineStuff()