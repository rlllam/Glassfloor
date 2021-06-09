from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://www.glassdoor.com/Job/canada-software-engineer-jobs-SRCH_IL.0,6_IN3_KO7,24_IP2.htm?includeNoSalaryJobs=true&pgc=AB4AAYEAHgAAAAAAAAAAAAAAAaemOL4AWgEBAQkArw6OeANTs1%2Fx1ozniMwa0AQaVTY3vcksGM1mUrj4Gc9md9VkgbqIvBZeOj0AWC2xQMieDAVU8a8aL1zCWYFEDZJc6RbH0gEdxUZI9Uqi9YDRSwSpswAA')

# WebDriver will wait 20 seconds until the next page button is found
# WebDriver will then store the element in "next_page_button"
next_page_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="FooterPageNav"]/div/ul/li[7]/a')))

next_page_button.click()