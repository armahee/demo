import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

def pre():
    os.system("pip install selenium==4.12.0")
    os.system("pip install undetected-chromedriver==3.5.3")
    os.system("pip install pandas==2.1.2")
    os.system("pip install chromedriver_autoinstaller==0.6.2")
    os.system("pip install beautifulsoup4==4.12.2")
    os.system("pip install pydrive==1.3.1")
if  not os.path.isfile(application_path+"/pre"):
    pre()
    f = open(application_path+"/pre","w")
    f.close()

import time
import chromedriver_autoinstaller
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path .dirname(__file__)
    
options = uc.ChromeOptions()
# options.headless = True
# options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={application_path}/seleniumdata")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--log-level=3")
options.add_argument("--no-first-run")
# options.add_argument("--disable-single-click-autofill")

gc_version = chromedriver_autoinstaller.get_chrome_version()
print("Chrome version:",gc_version)
driver = uc.Chrome(options=options,version_main=int(gc_version.split(".")[0]))

f_name = application_path+"/products.txt"
f = open(f_name, "r")
t_str = f.readlines()
f.close()

t_t = len(t_str)
t_i = 0


while t_i < 10:
    if driver.current_url[0:22] == "https://www.google.com":
        break
    l = t_str[t_i]
    t_i += 1
    print("running phase_____ "+str(t_i)+"/"+str(t_t))
    if len(l) < 27:
        continue
    link = l[0:len(l)-1]
    # time.sleep(30)
    driver.get(link)
    time.sleep(60)
    # exit()