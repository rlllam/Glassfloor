from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

JOB_SEARCH_BAR_ID = "sc.keyword"
LOCATION_SEARCH_BAR_ID = "sc.location"

JOB_LIST_ID = "MainCol"

JOB_DESC_CONTAINER_ID = "JobDescriptionContainer"
JOB_BOX_CLASS = "react-job-listing css-wp148e eigr9kq3"

SHOW_MORE_XPATH = "//div[@class='css-t3xrds e856ufb5']"

# Set webdriver to chrome
driver = webdriver.Chrome(PATH)
# Go on glassdoor
driver.get("https://www.glassdoor.com/bigppbrothers")

scrapped_job_desc = []

def scrap_job_dec(job_box):
    job_box.click()

    # WebDriver will wait until the job desciption is found
    try:
        job_description = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, JOB_DESC_CONTAINER_ID)))
    except:
        return "Timeout Error"

    # WebDriver will wait until the job desciption is found
    try:
        job_description = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, JOB_DESC_CONTAINER_ID)))
    except:
        return("Timeout Error")

    # Locate and click "Show More"
    show_more = job_description.find_element(By.XPATH, SHOW_MORE_XPATH)
    show_more.click()

    return job_description.text.split("\n")


def scrap_page():
    # WebDriver will wait until the job desciption is found
    try:
        job_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, JOB_LIST_ID)))
    except:
        return "Timeout Error"

    jobs = job_list.find_elements(By.CLASS_NAME, JOB_BOX_CLASS)

    for job in jobs:
        scrapped_job_desc += scrap_job_dec(job)


def scrap(job_title, job_location="Canada", num_of_jobs=5):
    """
    Returns the job description(s) of at least the
    specified number of related jobs posted on Glassdoor.
    """

    # Select the job search bar
    search = driver.find_element_by_id(JOB_SEARCH_BAR_ID)
    # Type the job title into the job search bar
    search.send_keys(job_title)
    # Select the location search bar
    search = driver.find_element_by_id(LOCATION_SEARCH_BAR_ID)
    # Type the location into the location search bar
    search.send_keys(job_location)
    # Press Enter
    search.send_keys(Keys.RETURN)

    while len(scrapped_job_desc) < num_of_jobs:
        scrapped_job_desc += scrap_page()

    return scrapped_job_desc


job_description = scrap("software")

# Sample formatted output
for index, paragraph in enumerate(job_description):
    print(str(index+1) + ".", paragraph, "\n")