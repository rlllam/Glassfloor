from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://www.glassdoor.com/bigppbrothers")

# Select the search bar
search = driver.find_element_by_id("sc.keyword")

# Type the keyword into the search bar and press enter
keyword = "Space Vehicle Controller/Engineer - Entry Level"
search.send_keys(keyword)
search.send_keys(Keys.RETURN)

time.sleep(10)

clickThis = driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb5']")
clickThis.click()

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "JobDescriptionContainer"))
    )
except:
	print("not found")
	# driver.quit()

paragraphs = element.find_elements_by_tag_name("p")
for paragraph in paragraphs:
    print(paragraph.text)

# try:
#     print(str(driver.page_source))
# except:
#     print("error")
