from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.glassdoor.com/bigppbrothers")

# Select the search bar
search = driver.find_element_by_id("sc.keyword")

# Type the keyword into the search bar and press enter
keyword = "Space Vehicle Controller/Engineer - Entry Level"
search.send_keys(keyword)
search.send_keys(Keys.RETURN)

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