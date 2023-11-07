import os
import sys
import time
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import undetected_chromedriver as uc
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

f_name = "products.txt"
f = open(f_name, "r")
links = f.readlines()
f.close()
f_name = "cat.txt"
f = open(f_name, "r")
t_str = f.readlines()
f.close()
t_t = len(t_str)
t_i = 0
f_name = "products.txt"
f = open(f_name, "a")
tcnt = len(links)
while t_i < 1:
    l = t_str[t_i]
    t_i += 1
    print("running phase_____ "+str(t_i)+"/"+str(t_t))
    if len(l) < 27:
        continue
    link = l[0:len(l)-1]
    time.sleep(30)
    print("starting")
    driver.get(link)
    time.sleep(60)
    exit()
    print("scraping")
    fl = True
    while fl:
        if driver.current_url[0:22] == "https://www.google.com":
            break
        cnt = 0
        pcnt = 0
        try:
            soup = BeautifulSoup(driver.page_source,"html.parser")
            anchs = soup.find_all("a",{"href":True})
            for a in anchs:
                if len(a.get("href")) > 3:
                    if a.get("href")[0:3] == "/p/":
                        fl1 = True
                        for c in links:
                            if "https://www.coursesu.com"+a.get("href")+"\n" == c:
                                fl1 = False
                                break
                        if fl1:
                            cnt += 1
                            links.append("https://www.coursesu.com"+a.get("href")+"\n")
                            f.write("https://www.coursesu.com"+a.get("href"))
                            f.write("\n")
                            f.flush()
            tcnt += cnt
            print("found:",cnt,"/",tcnt)

        except Exception as e:
            print('error scraping')
            print(e)
        if cnt > 0:
            pcnt = cnt
            data_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html')
                )
            )
            data_text.send_keys(Keys.END,Keys.PAGE_UP,Keys.PAGE_UP)
    print("ok")

f.close()