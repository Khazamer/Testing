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

import traceback

# COLORING SCHEME
# Magenta: Major steps/progress
# Yellow: Settings and other control

def gatherFacebook(places, settings):
    
    # Setting up the browser
    # region
    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass the sandbox (needed for Docker)
    options.add_argument("--disable-dev-shm-usage")  # Overcome Docker’s memory limitations
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--enable-unsafe-swiftshader')
    options.add_argument("--log-level=3")  # Suppresses all logs except critical errors
    options.page_load_strategy = "none" # SUPER IMPORTANT FOR SPEED - allows us to load all locations so they start loading faster

    #options.browser_version = '114' # says that the chrome driver only supports version 114

    # Initialize the WebDriver with the configured options
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    # endregion

    print("Starting Up")

    first_tab = driver.window_handles[0]

    # Setup multiple tabs
    for place in places:
        driver.switch_to.new_window() 
        newLink = "https://www.facebook.com/marketplace/" + place + "/search?query=vehicles&radius=1&daysSinceListed=1&sortBy=creation_time_descend"
        #print(newLink)
        driver.get(newLink)

    print(f"{Fore.LIGHTMAGENTA_EX}{len(places)} tabs open and setup")
    print(f"{Fore.LIGHTYELLOW_EX}Settings")
    print(f"{Fore.YELLOW}Clear Alerts = {settings['clear alerts']} | {Fore.YELLOW}Scroll = {settings['scroll']}")

    driver.switch_to.window(first_tab)
    driver.close()

    listings = []
    scroll_broke = False

    print(f"{Fore.LIGHTMAGENTA_EX}Progress:     {Fore.YELLOW}Loaded  {Fore.RED}Alerts  {Fore.BLUE}Scrolled  {Fore.CYAN}Found  {Fore.GREEN}Real")

    handles = driver.window_handles
    for i, handle in enumerate(handles):
        driver.switch_to.window(handle)

        progress_str = ""
        progress_str = f"{Fore.MAGENTA}Search {i+1} of {len(handles)}:"
        print(progress_str, end='\r')

        """ # doesn't work cuz of selenium have predefined definitions
        try:
            WebDriverWait(10, driver).until(driver.execute_script("return document.readyState") == "complete") # need to see if this works
            # doesn't work, need another system to check
            # may just use while loop tbh
        except:
            print("Page faled to load")
            pass
        """

        check_timer = 10 # this works but may change tbs
        while check_timer:
            check = driver.execute_script("return document.readyState") == "complete"
            #print(check)
            if check:
                break
            time.sleep(1)
            check_timer -= 1

        #print(f"{Fore.CYAN}{i+1}: Page loaded")
        progress_str += f"  {Fore.YELLOW}\u2713"
        print(progress_str, end='\r')

        if settings["clear alerts"]: # clear the alerts
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Decline optional cookies']"))).click()
            except:
                print("wrong page") # may want to add a reload system down the line
                continue

            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Close']"))).click()
            except:
                print("no login filter")

            #print(f"{Fore.CYAN}{i+1}: Alerts cleared")
            progress_str += f"       {Fore.RED}\u2713"
            print(progress_str, end='\r')

            if settings["scroll"]: # scroll down the page
                progress_str += f"    {Fore.BLUE}Scrolling"
                print(progress_str, end='\r')
                progress_str = progress_str[:-13]
                try:
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    while(True):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(5)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if last_height == new_height:
                            break
                        last_height = new_height
                    #print(f"{Fore.CYAN}{i+1}: Scrolled")
                    progress_str += f"    {Fore.BLUE}Scrolling"
                    print(progress_str, end='\r')
                    progress_str = progress_str[:-13]
                except:
                    #print(f"{Fore.CYAN}{i+1}: Scroll Broke")
                    progress_str += f"            {Fore.BLUE}X"
                    print(progress_str, end='\r')

                    scroll_broke = True

                if not scroll_broke:
                    #print(f"{Fore.CYAN}{i+1}: Scroll Done")
                    print(progress_str, end='\r')
                    time.sleep(5)
                    progress_str += f"            {Fore.BLUE}\u2713"
                    print(progress_str, end='\r')

            else:
                progress_str += f"        {Fore.BLUE}NA"
                print(progress_str, end='\r')

        else:
            progress_str += f"       {Fore.RED}NA        {Fore.BLUE}NA"
            print(progress_str, end='\r')

        #time.sleep(30) #x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24

        time.sleep(0.1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file = open("testing.txt", 'w', encoding="utf-8")
        file.write(soup.prettify())
        file.close

        located = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
        #print(f'{Fore.CYAN}{i+1}: Num Listings Found: {len(located)}')

        progress_str += f"       {Fore.CYAN}{len(located)}"
        print(progress_str, end='\r')

        listings_temp = []
        temp_error_recall = ""

        for listing in located:
            each = {}
            try:
                #url = "https://www.facebook.com" + listing.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv")['href']
                url = "https://www.facebook.com" + listing.find('a')['href'] # since there is 1 a class this is an even easier solution
                listing_num = url[url.find("item/")+5:url.find("/?ref")]
                #image = listing.find('img', class_='x168nmei x13lgxp2 x5pf9jr xo71vjh xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
                image = listing.find('img')['src'] # same here since theres only 1 img class
                '''
                title = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
                price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text # diff on docker for some reason: x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u
                locationAndMiles = listing.find_all('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
                location = locationAndMiles[0].text
                miles = locationAndMiles[1].text
                '''
                # we can mess with built in functionality of finding class names and attributes
                spans = listing.find_all('span')
                title = spans[5].text
                price = spans[2].text
                location = spans[8].text
                miles = spans[10].text
                # can also make this self healing but should be good for now

                each["Listing_ID"] = listing_num
                each["Listing URL"] = url #"https://www.facebook.com" + url
                each["Image URL"] = image
                each["Title"] = title
                each["Visible_Price"] = price
                each["Location"] = location
                each["Miles"] = miles
                each["Search Origin"] = location
                each["Search Site"] = "Facebook"

                listings_temp.append(each)

            except Exception as error:
                #print(error)
                #print(traceback.format_exc())
                if not temp_error_recall:
                    temp_error_recall = traceback.format_exc()
                    temp_soup = listing
                pass
        
        #print(f'{Fore.CYAN}{i+1}: Actual Listings Count: {len(listings_temp)}')
        progress_str += f"    {Fore.GREEN}{len(listings_temp)}"
        print(progress_str)
        if (len(listings_temp) == 0):
            print(temp_error_recall)
            print(temp_soup)

        listings += listings_temp

        # Using in browser search (not working for some reason)
        '''
        # change gathering to be in browser to save space (and money)
        # some issue with being unable to find classes that clearly exist on facebook
        # need to look into this and do some testing
        # rest of the stuff should work but will also test
        located_listings = driver.find_elements(By.CLASS_NAME, "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24")
        print(f"{Fore.MAGENTA}Listings found: {len(located_listings)}")

        listings = []
        for listing in located_listings: # WILL NEED TO UPDATE THESE VALUES OVERTIME SO MAKE SURE TO UPDATE THEM IF YOU RUN INTO ANY ERRORS
            each = {}
            try:
                #url = "https://www.facebook.com" + listing.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")['href']
                url = "https://www.facebook.com" + listing.find_element(By.CSS_SELECTOR, '[role="link"]').get_attribute("href")
                listing_num = url[url.find("item/")+5:url.find("/?ref")]
                #image = listing.find('img', class_='xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
                image = listing.find_element(By.CSS_SELECTOR, '[referrerpolicy="origin-when-cross-origin"]').get_attribute("src")
                #title = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
                title = listing.find_element(By.CLASS_NAME, "x1lliihq x6ikm8r x10wlt62 x1n2onr6").text
                #price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
                price = listing.find_element(By.CLASS_NAME, "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u").text
                #locationAndMiles = listing.find_all('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
                locationAndMiles = listing.find_elements(By.CLASS_NAME, "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
                location = locationAndMiles[0].text
                miles = locationAndMiles[1].text

                each["Listing_ID"] = listing_num
                each["Listing URL"] = url #"https://www.facebook.com" + url
                each["Image URL"] = image
                each["Title"] = title
                each["Visible_Price"] = price
                each["Location"] = location
                each["Miles"] = miles
                each["Search Origin"] = location
                each["Search Site"] = "Facebook"

                listings.append(each)

            except Exception as error:
                #print(error)
                print(traceback.format_exc())
                #print(f"{Fore.CYAN}{location}: {Fore.RED}Listing error: {error}")
                pass

        print("done")

    print("done all")
    '''
                
    driver.quit()

    # May not be needed
    del soup
    del located
    del listings_temp

    print(f'{Fore.MAGENTA}Total Listings Found: {len(listings)}')

def addPic(id, link):
    picPath = 'images/' + str(id) + '.jpg'
    urlretrieve(link, picPath)

    dir_list = os.listdir('images/')
    print(dir_list)
    print(len(dir_list))

# Running stuff
settings = {
    "clear alerts": True,
    "scroll": False,
}

places = [
    "pittsburgh",
    "cleveland",
    "columbus",
    "westwheeling"
]

# all places
# erie, lancaster, morgantown

gatherFacebook(places=places, settings=settings)

#driver.find_element(By.XPATH, "//div[contains(@aria-label,'Log In')]/div/div").click()

"""
TO RUN
docker build -t test .
docker run -d --name test_container test # need to remove this container before running it again
"""