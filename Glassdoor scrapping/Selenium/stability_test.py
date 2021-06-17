# import os
# from subprocess import *
from subprocess import Popen

# Use a VPN for this because Glassdoor will probably block your ip after testing for a while

for i in range(10):
	Popen("python Selenium_glassdoor_scrapper.py", shell=True)