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

link = "https://images.all-free-download.com/images/thumbjpg/test_testing_optical_265619.jpg"

addPic(link)