from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriver 90.0.4430.24
PATH = "C:\Program Files (x86)\chromedriver.exe"

"""
In "JOB_BOX_COMMON_XPATH_SYNTAX":
1. 'li' has indices that start from 1.
2. If 'li' is provided an index, the XPATH references a clickable job box.
3. If 'li' is not provided an index, or is provided with [1:], the XPATH references all indices
"""
JOB_BOX_COMMON_XPATH_SYNTAX = "//*[@id='MainCol']/div[1]/ul/li"

SIGN_UP_PROMPT_XPATH = "//*[@id='JAModal']/div/div[2]"

JOB_DESC_CONTAINER_ID = "JobDescriptionContainer"

SHOW_MORE_XPATH = "//*[@id='JobDescriptionContainer']/div[2]"

PAGE_BUTTON_XPATH_COMMON_SYNTAX = "//*[@id='FooterPageNav']/div/ul/li"

# Set webdriver to chrome
driver = webdriver.Chrome(PATH)
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
    Ensures the sign up prompt is closed.
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
    Clicks the 'Show More' button.
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

def scrap_job_desc(job_box):
    """
    Returns the job description of the job box as a string.
    """
    job_box.click()

    click_show_more()

    while True:
        try:
         # WebDriver will wait 20 seconds until the job desciption is found and store it
            job_description = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, JOB_DESC_CONTAINER_ID)))
            return job_description.text # Return statement sometimes raises StaleElementReferenceException

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

            # Ensuring the next page is reached
            while driver.current_url == old_url:
                continue

            return True

        # If there is an exception, refresh the current page and retry
        except:
            driver.get(driver.current_url)

def scrap_page():
    """
    Returns all job descriptions on the current page as an array of strings.
    """
    while True:
        try:
            # WebDriver will wait 30 seconds until the job box list is found and store it
            job_box_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, JOB_BOX_COMMON_XPATH_SYNTAX)))

            # Put all job descriptions into 'scrapped_page'
            scrapped_page = []

            for idx in range(len(job_box_list)):
                job_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, JOB_BOX_COMMON_XPATH_SYNTAX+ "[" + str(idx+1) + "]")))

                scrapped_page.append(scrap_job_desc(job_box))
                print("Jobs scrapped: " + str(idx+1))

            break

        # If there is an exception, refresh the current page and retry
        except:
            driver.get(driver.current_url)
    

    return scrapped_page

def scrap(keyword, location, pages_to_scape=1):
    """
    Returns an array of job descriptions as strings.
    """
    print("Starting...")
    start_time = time.time()

    # Go on the desired glassdoor search results page
    driver.get("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="
        + keyword +
        "&typedLocation=" + location +
        "&locT=N&locId=3&jobType=&context=Jobs&sc.keyword=Software+Engineer&dropdown=0")

    scrapped_job_descriptions = []

    for i in range(pages_to_scape):
        print(f"\nScrapping page {str(i+1)}...\n")

        scrapped_job_descriptions += scrap_page()
        pages_scaped = i+1

        if pages_scaped < pages_to_scape:
            page_exist = go_to_next_page()
            if not page_exist:
                break

    # Record time it took to run scrap()
    time_taken = time.time() - start_time
    print("\n" + str(len(scrapped_job_descriptions)) + " entries in total\nTime Taken: " + str(time_taken))

    return scrapped_job_descriptions



"""
1. Scrap job descriptions on glassdoor by providing: keyword, location, pages_to_scrape (default is 1).
2. Store the resulting array in 'scrapped_desc'.
"""
scrapped_desc = scrap('software', 'canada', 10)
driver.quit()

# Format the output and print it
# for idx, job_desc in enumerate(scrapped_desc):
#         print(str(idx+1) + ". " + job_desc + "\n")