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
    """
    id = random.randint(1, 10)

    picPath = 'images/' + str(id) + '.jpg'

    urlretrieve(link, picPath)

    print(picPath)
    """
    picPath = 'images/' + '1' + '.jpg'
    urlretrieve(link, picPath)
    picPath = 'images/' + '2' + '.jpg'
    urlretrieve(link, picPath)

    dir_list = os.listdir('images/')
    #print(len(os.listdir('images/')))
    print(dir_list)
    print(len(dir_list))

    print("done with 1")

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
    print("into web system")

    #Set up Chrome options for headless mode
    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass the sandbox (needed for Docker)
    options.add_argument("--disable-dev-shm-usage")  # Overcome Docker’s memory limitations
    options.add_argument("--disable-notifications")

    options.browser_version = '114' # says that the chrome driver only supports version 114

    print("options done")

    # Initialize the WebDriver with the configured options
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)

    print("browser setup")

    driver.get("https://www.google.com/")

    time.sleep(5)

    print(driver.title)

# testing stuff

link = "https://images.all-free-download.com/images/thumbjpg/test_testing_optical_265619.jpg"

#addPic(link)

#print("Picture done")

#getOnlineStuff()

#print("online stuff done")

#multithreadGoogle() # requires other stuff to work, may implement down the line

"""
with psycopg2.connect(
        host = database_config['hostname'],
        dbname = database_config['database name'],
        user = database_config['username'],
        password = database_config['pass'],
        port = database_config['port id']
    ) as conn:

        # Create cursor object
        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur: # creates a cursor object which returns SELECT query values as dictionaries
"""
"""
with psycopg2.connect(
    host = "34.56.131.167",
    dbname = "vehicles",
    user = "dev_test",
    password = "testing_time_for_now_dev",
    port = 5432
) as conn:
    with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
        # stuff goes here
        test_q = "SELECT * FROM cars" # make cars table first and make sure to spin up db
        cur.execute(test_q)
        things = cur.fetchall()
        print(things)
"""

# Testing for scrape

import traceback

def testing1Scrape(places, settings):
    
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
    print(f"{Fore.YELLOW}Clear Alerts = {settings['clear alerts']}")
    print(f"{Fore.YELLOW}Scroll = {settings['scroll']}")

    driver.switch_to.window(first_tab)
    driver.close()

    listings = []

    handles = driver.window_handles
    for i, handle in enumerate(handles):
        driver.switch_to.window(handle)

        print(f"{Fore.LIGHTCYAN_EX}Search {i+1} of {len(handles)}")

        """
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

        print(f"{Fore.CYAN}{i+1}: Page loaded")

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

            print(f"{Fore.CYAN}{i+1}: Alerts cleared")

            if settings["scroll"]: # scroll down the page
                try:
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    while(True):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(5)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if last_height == new_height:
                            break
                        last_height = new_height
                    print(f"{Fore.CYAN}{i+1}: Scrolled")
                except:
                    print(f"{Fore.CYAN}{i+1}: Scroll Broke")

                print(f"{Fore.CYAN}{i+1}: Scroll Done")

        #time.sleep(30) #x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24

        time.sleep(0.1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file = open("testing.txt", 'w', encoding="utf-8")
        file.write(soup.prettify())
        file.close

        located = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
        print(f'{Fore.CYAN}{i+1}: Num Listings Found: {len(located)}')

        listings_temp = []
        temp_error_recall = ""

        for listing in located: # WILL NEED TO UPDATE THESE VALUES OVERTIME SO MAKE SURE TO UPDATE THEM IF YOU RUN INTO ANY ERRORS
            each = {}
            try: # curr class name: x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv
                url = "https://www.facebook.com" + listing.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv")['href']
                listing_num = url[url.find("item/")+5:url.find("/?ref")]
                image = listing.find('img', class_='xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
                title = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
                price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
                locationAndMiles = listing.find_all('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
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

                listings_temp.append(each)

            except Exception as error:
                #print(error)
                #print(traceback.format_exc())
                if not temp_error_recall:
                    temp_error_recall = traceback.format_exc()
                pass
        
        print(f'{Fore.CYAN}{i+1}: Actual Listings Count: {len(listings_temp)}')
        if (len(listings_temp) == 0):
            print(temp_error_recall)

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

#testing1Scrape(places=places, settings=settings)

#driver.find_element(By.XPATH, "//div[contains(@aria-label,'Log In')]/div/div").click()

# NEW IDEA
# new url sorts by time and gets the newest cars fastest
#"https://www.facebook.com/marketplace/pittsburgh/search?query=vehicles&radius=1&daysSinceListed=1&sortBy=creation_time_descend"

# Notes
# There is a list of all possible cars

"""
<div class="x78zum5 xdt5ytf x11tup63 x16z1lm9">
                <div class="xwoyzhm x1rhet7l">
                <span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u x1yc453h" dir="auto">
                <h1 class="html-h1 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1vvkbs x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz">
                    <span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 xngnso2 x1qb5hxa x1xlr1w8 xzsf02u">
                    Vehicles Near Pittsburgh, Pennsylvania
                    </span>
                </h1>
                </span>
                </div>
                </div>

<a class="x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x18d9i69 x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x1tlxs6b x1g8br2z x1gn5b1j x230xth x78zum5 x1q0g3np xc9qbxq xl56j7k xn6708d x1ye3gou x1n2onr6 xh8yej3 x1qhmfi1" href="/marketplace/pittsburgh/aston-martin-db9/" role="link" tabindex="0">
                      <span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xzsf02u" dir="auto">
                       <span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft">
                        Aston Martin Db9
                       </span>
                      </span>
                      <div class="x1ey2m1c xds687c x17qophe xg01cxk x47corl x10l6tqk x13vifvy x1ebt8du x19991ni x1dhq9h x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m" data-visualcompletion="ignore" role="none">
                      </div>
                     </a>
"""

# console test
'''
import time
import sys

# Function to print loading bar
def loading_bar(progress, total, width=40):
    # Calculate the percentage of progress
    percentage = (progress / total)
    
    # Create a string of the current progress
    num_hashes = int(percentage * width)
    num_spaces = width - num_hashes
    
    # Create the loading bar string
    bar = f"[{'#' * num_hashes}{' ' * num_spaces}] {percentage * 100:.2f}%"
    
    # Print the loading bar on the same line
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()

# Example usage of the loading bar
total_steps = 100

for step in range(total_steps + 1):
    loading_bar(step, total_steps)
    time.sleep(0.1)  # Simulate work being done

print()  # Newline after loading bar completion
'''
'''
import time
import sys

# Function to print loading bars
def loading_bars(progress, total, num_bars=3, width=40):
    # Create a string for each loading bar
    bars = []
    for i in range(num_bars):
        # Calculate the percentage of progress for each bar
        percentage = (progress + i) / total
        num_hashes = int(percentage * width)
        num_spaces = width - num_hashes
        
        # Create each loading bar
        bar = f"[{'#' * num_hashes}{' ' * num_spaces}] {percentage * 100:.2f}%"
        bars.append(bar)
    
    # Clear the screen and print the loading bars
    sys.stdout.write('\r' + '\n'.join(bars) + '\r')
    sys.stdout.flush()

# Example usage of the loading bars
total_steps = 100

for step in range(total_steps + 1):
    loading_bars(step, total_steps)
    time.sleep(0.1)  # Simulate work being done

print()  # Newline after loading bar completion
'''

print('\u2713 and hello there')
print(f'{Fore.CYAN} \u2713 {Fore.WHITE} and hello there')
temp = f"{Fore.YELLOW} hi there"
print(temp)
temp += f"{Fore.GREEN} yo"
print(temp)
print(f"{Fore.BLACK} hello")
print(f"{Fore.BLUE} hello")
print(f"{Fore.YELLOW} hello")
print(f"{Fore.RED} hello")
print(f"{Fore.GREEN} hello")
print(f"{Fore.CYAN} hello")
print(f"{Fore.MAGENTA} hello")
print(f"{Fore.WHITE} hello")

# CURSES
# Useful but idk how much in this case since we will want terminal output
# It write on its own screen so we wont see it anyways when runnign on google
'''
import curses
from curses import wrapper

def cursesSetup(stdscr):
    stdscr.clear()

    stdscr.addstr("hi")
    stdscr.addstr(10, 10, "hi") # choose loc on screen

    stdscr.refresh()
    stdscr.getch()

wrapper(cursesSetup)
'''

# Extras

"""
TO RUN
docker build -t test .
docker run -d --name test_container test # need to remove this container before running it again
"""