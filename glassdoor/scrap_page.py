from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

start_time = time.time()

PATH = "C:\Program Files (x86)\chromedriver.exe"

JOB_SEARCH_BAR_ID = "sc.keyword"
LOCATION_SEARCH_BAR_ID = "sc.location"

"""
In "JOB_BOX_COMMON_XPATH_SYNTAX":
1. "li" has indices that start from 1.
2. If "li" is provided an index, the XPATH references a clickable job box.
3. If "li" is not provided an index, the XPATH references all indices
"""
JOB_BOX_COMMON_XPATH_SYNTAX = "//*[@id='MainCol']/div[1]/ul/li"

SIGN_UP_PROMPT_XPATH = "//*[@id='JAModal']/div/div[2]"

JOB_DESC_CONTAINER_ID = "JobDescriptionContainer"

SHOW_MORE_XPATH = "//*[@id='JobDescriptionContainer']/div[2]"

# Set webdriver to chrome
driver = webdriver.Chrome(PATH)
# Go on glassdoor
driver.get("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software&typedLocation=Canada&locT=N&locId=3&jobType=&context=Jobs&sc.keyword=Software+Engineer&dropdown=0")


def check_exists_by_xpath(xpath):
    """Check if an element exists by xpath"""

    try:
        driver.find_element_by_xpath(xpath)
    except exceptions.NoSuchElementException:
        return False
    return True


def close_sign_up():
    """Ensures the sign up prompt is closed"""

    while check_exists_by_xpath(SIGN_UP_PROMPT_XPATH):
        # Press "Esc" globally
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def click_show_more(show_more):
    """Clicks the "Show More" button"""

    try:
        show_more.click()

    # Cannot click "Show More" due to sign up prompt
    except exceptions.ElementClickInterceptedException:
        close_sign_up()
        click_show_more(show_more)

    # The reference to the element became invalid
    except exceptions.StaleElementReferenceException:
        # Re-instantiate the reference
        show_more = driver.find_element(By.XPATH, SHOW_MORE_XPATH)
        show_more.click()


def scrap_job_desc(job_box):
    """Returns the job description of the job box as a string"""

    job_box.click()

    #  WebDriver will wait 20 seconds until "Click More is found"
    show_more = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, SHOW_MORE_XPATH)))

    click_show_more(show_more)

    # WebDriver will wait 20 seconds until the job desciption is found
    job_description = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, JOB_DESC_CONTAINER_ID)))

    return job_description.text


def scrap_page():
    """
    Returns all job descriptions on the current page as an array of strings.
    """

    # WebDriver will wait 20 seconds until the job box list is found
    job_box_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, JOB_BOX_COMMON_XPATH_SYNTAX)))

    # Put all job descriptions into "scrapped_page"
    scrapped_page = []
    for job_box in job_box_list:
        scrapped_page.append(scrap_job_desc(job_box))

    return scrapped_page


job_desc_list = scrap_page()
driver.close()
time_taken = time.time() - start_time

for index, job_desc in enumerate(job_desc_list):
    print(str(index+1) + ". " + job_desc + "\n")

print(str(len(job_desc_list)) + " entries in total\nTime Taken: " + str(time_taken))