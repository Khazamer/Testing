import undetected_chromedriver as uc

import time

options = uc.ChromeOptions()
#options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")  # Bypass the sandbox (needed for Docker)
options.add_argument("--disable-dev-shm-usage")  # Overcome Docker’s memory limitations
options.add_argument("--disable-notifications")

#uc.TARGET_VERSION = 85
driver = uc.Chrome(version_main=132, options=options)
#driver = uc.Chrome()
#driver.get('https://distilnetworks.com')
#driver.get('https://google.com')
#driver.get("https://www.facebook.com/marketplace/pittsburgh/search?query=vehicles&radius=1&daysSinceListed=1&sortBy=creation_time_descend")
#driver.get("https://facebook.com/marketplace/")
#driver.get("https://www.facebook.com/marketplace/")

# Make tabs
for i in range(0,3):
    driver.switch_to.new_window()

handles = driver.window_handles
handles = handles[1:]

driver.switch_to.window(handles[0])

time.sleep(2)

driver.close()

time.sleep(2)

driver.close()

time.sleep(2)

driver.close()

time.sleep(60)