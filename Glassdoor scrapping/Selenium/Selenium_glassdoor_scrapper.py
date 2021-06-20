# This script was made on ChromeDriver 90.0.4430.24
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

"""
In "JOB_BOX_COMMON_XPATH_SYNTAX":
1. 'li' has indices that start from 1.
2. If 'li' is provided an index, the XPATH references a clickable job box.
3. If 'li' is not provided an index, or is provided with [1:], the XPATH references all indices
"""
JOB_BOX_COMMON_XPATH_SYNTAX = "//*[@id='MainCol']/div[1]/ul/li"
SIGN_UP_PROMPT_XPATH = "//*[@id='JAModal']/div/div[2]"
SHOW_MORE_XPATH = "//*[@id='JobDescriptionContainer']/div[2]"
PAGE_BUTTON_XPATH_COMMON_SYNTAX = "//*[@id='FooterPageNav']/div/ul/li"

COMPANY_NAME_XPATH_1 = "//*[@id='MainCol']/div[1]/ul/li["
COMPANY_NAME_XPATH_2 = "]/div[2]/div[1]/a/span"

JOB_TITLE_XPATH = "//*[@id='JDCol']/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]"
JOB_LOCATION_XPATH = "//*[@id='JDCol']/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]"
OVERALL_RATING_XPATH = "//*[@id='JDCol']/div/article/div/div[1]/div/div/div[1]/div/div[1]/div[1]/span"

ESTIMATED_SALARY_XPATH_1 = "//*[@id='MainCol']/div[1]/ul/li["
ESTIMATED_SALARY_XPATH_2 = "]/div[2]/div[3]/div[1]/span"

EASY_APPLY_XPATH = "//*[@id='JDCol']/div/article/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/span/button/span"

# Examples: "HOT", NEW", "TOP COMPANY", "HIRING SURGE"
SPECIAL_LABEL_XPATH = "//*[@id='PrimaryModule']/div/span[1]"

JOB_DESC_CONTAINER_ID = "JobDescriptionContainer"


def handle_error(error):
    '''
    A general approach to handle any error
    '''
    print("\nError:\n" + str(error) + "\n\nHandling error...\n")

    # Refresh current page
    driver.get(driver.current_url)

    # Get width and height of the current window
    current_size = driver.get_window_size()
    width, height = current_size['width'], current_size['height']

    # Increase the current window width and height by 10 pixels (so Selenium can see more)
    driver.set_window_size(width+10, height+10)

    # Option to minimize window
    driver.minimize_window()

def check_exists_by_xpath(xpath):
    """
    Check if an element exists by xpath.
    """
    try:
        driver.find_element_by_xpath(xpath)
    except exceptions.NoSuchElementException:
        return False
    return True

def close_sign_up():
    """
    Ensures the sign up prompt is closed
    """
    while check_exists_by_xpath(SIGN_UP_PROMPT_XPATH):
        # Press 'Esc' globally
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def instantiate_show_more():
    """
    Instantiate reference to the show more button and store it into 'show more'.
    Retry indefinitely until it works.
    """
    instantiate_successfully = False

    while not instantiate_successfully:
        try:
            show_more = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, SHOW_MORE_XPATH)))

            instantiate_successfully = True

        except exceptions.StaleElementReferenceException:
            pass

    return show_more

def click_show_more():
    """
    Ensures the 'Show More' button is clicked
    """
    try:
        show_more = instantiate_show_more()
        show_more.click()

    # Cannot click 'Show More' due to sign up prompt
    except exceptions.ElementClickInterceptedException:
        close_sign_up()
        click_show_more()

    # The reference to the element became invalid
    except exceptions.StaleElementReferenceException:
        # Try again
        click_show_more()

def scrape_job(job_box, job_num):
    """
    Returns the job description of the job box as a string
    job_box: The job box element
    job_num: The order of the job in the list
    """
    job_box.click()

    click_show_more()

    while True:
        try:
            job_info = {}

            # If the job description is loaded then everything else should be loaded
            job_desc = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, JOB_DESC_CONTAINER_ID))).text

            job_info['Company'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, COMPANY_NAME_XPATH_1 + str(job_num) + COMPANY_NAME_XPATH_2))).text
            job_info['Job Title'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, JOB_TITLE_XPATH))).text
            job_info['Location'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, JOB_LOCATION_XPATH))).text
            job_info['Overall Rating'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, OVERALL_RATING_XPATH))).text if check_exists_by_xpath(OVERALL_RATING_XPATH) else None

            estimated_salary_xpath = ESTIMATED_SALARY_XPATH_1 + str(job_num) + ESTIMATED_SALARY_XPATH_2
            job_info['Employer Estimated Salary'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, estimated_salary_xpath))).text if check_exists_by_xpath(estimated_salary_xpath) else None

            job_info['Easy Apply'] = True if check_exists_by_xpath(EASY_APPLY_XPATH) else False
            job_info['Special Label'] = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, SPECIAL_LABEL_XPATH))).text if check_exists_by_xpath(SPECIAL_LABEL_XPATH) else None
            job_info['Job Age'] = job_box.text.split('\n')[-1]
            job_info['Job Description'] = job_desc

            return job_info

        except exceptions.StaleElementReferenceException:
            pass

def go_to_next_page():
    """
    Ensures the next page is reached
    """
    while True:
        try:
            page_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, PAGE_BUTTON_XPATH_COMMON_SYNTAX)))

            # The Xpath of the next page button is //*[@id='FooterPageNav']/div/ul/li[*last index*]
            next_page_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, PAGE_BUTTON_XPATH_COMMON_SYNTAX + "[" + str(len(page_list)) + "]")))

            button_is_disabled = next_page_button.get_attribute("disabled")

            # Already reached the last page
            if button_is_disabled:
                return False

            old_url = driver.current_url
            next_page_button.click()

            # Ensure the next page is reached
            while driver.current_url == old_url:
                continue

            # Alternatively (not tested):
            # WebDriverWait(driver, 15).until(EC.url_changes(driver.current_url))

            return True

        except Exception as e:
            handle_error(e)

def scrap_page():
    """
    Returns the information of each job on the current page as a list of dictionaries
    """
    while True:
        try:
            # WebDriver will wait 30 seconds until the job box list is found and store it
            job_box_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, JOB_BOX_COMMON_XPATH_SYNTAX)))

            # Put the information of each job as dictionaries into 'scrapped_page'
            scrapped_page = []

            for idx in range(len(job_box_list)):
                job_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, JOB_BOX_COMMON_XPATH_SYNTAX+ "[" + str(idx+1) + "]")))

                scrapped_page.append(scrape_job(job_box, idx+1))
                print("Jobs scrapped: " + str(idx+1))

            break

        except Exception as e:
            handle_error(e)
    
    return scrapped_page

def scrap(keyword, location, pages_to_scrape=1):
    """
    Returns a list of job information as dictionaries
    """
    print("Starting...")
    start_time = time.time()

    # Go on the desired glassdoor search results page
    driver.get("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="
        + keyword +
        "&typedLocation=" + location +
        "&locT=N&locId=3&jobType=&context=Jobs" +
        "&sc.keyword=" + keyword + "&dropdown=0")

    scrapped_jobs = []

    for i in range(pages_to_scrape):
        print(f"\nScrapping page {str(i+1)}...\n")

        scrapped_jobs += scrap_page()
        pages_scaped = i+1

        if pages_scaped < pages_to_scrape:
            page_exist = go_to_next_page()
            if not page_exist:
                print("Last page reached")
                break

    # driver.quit()

    # Record time it took to run scrap()
    time_taken = time.time() - start_time
    print("\nTotal jobs scrapped: " + str(len(scrapped_jobs)) + "\nTime Taken: " + str(time_taken))

    return scrapped_jobs


if __name__ == '__main__':
    # ChromeDriver 90.0.4430.24
    DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

    '''
    Headless option
    '''
    # from selenium.webdriver.chrome.options import Options
    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1275,1030") # Smallest size such that Selenium can see everything
    # driver = webdriver.Chrome(DRIVER_PATH, options=options)

    '''
    Default option
    '''
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.minimize_window() # Option to start minimized


    # Parameters for main function
    keyword = 'Software'
    location = 'Canada'
    pages_to_scrape = 1

    # Run main function
    scrapped_jobs = scrap(keyword=keyword, location=location, pages_to_scrape=pages_to_scrape)


    # Create dataframe
    df = pd.DataFrame.from_dict(scrapped_jobs)

    # Export
    df.to_csv('scrapped jobs - ' + keyword + ', ' + location + '.csv', index=False)
