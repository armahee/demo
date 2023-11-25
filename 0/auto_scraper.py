import os
import datetime
import re
import random
import sys
import time
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse
import chromedriver_autoinstaller
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import tkinter as tk
from tkinter import messagebox

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path .dirname(__file__)


options = Options()
# options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f"--user-data-dir={application_path}/seleniumdata")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--log-level=3")
options.add_argument("--no-first-run")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument("disable-infobars")
# options.add_argument("--disable-single-click-autofill")

gc_version = chromedriver_autoinstaller.get_chrome_version()
print("Chrome version:",gc_version)
driver = webdriver.Chrome(options=options)#,version_main=int(gc_version.split(".")[0]))
# time.sleep(60)
# exit()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
})
# driver.set_page_load_timeout(10)
file_out = ''

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False
    

def msgbox(message):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo('Info',message)
    root.destroy()

def get_value(data,path):
    try:
        return eval(f"{data}{path}")
    except:
        return ''

def write_csv(data):

    csv_exist = os.path.isfile(file_out)
    with open(file_out, 'a',newline='',encoding='utf-8') as outfile:
        headers = ['Title','E-mail','Location']
        writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
        if not csv_exist:
            writer.writerow(headers)

        writer.writerow(data)

def get_product_data(name,city):
    if type(name) == type(float()):
        name = ''
    if type(city) == type(float()):
        city = ''
    sname = '%26'.join(name.split('&'))
    scity = '%26'.join(city.split('&'))
    sname = '+'.join(sname.split(' '))
    scity = '+'.join(scity.split(' '))
    url = "https://www.google.com/search?q="+sname+'+'+scity+"+ie"
    time.sleep(3)
    driver.get(url)
    fsoup = BeautifulSoup(driver.page_source,"html.parser")
    gsoup = fsoup.find_all("div",{"id":"search"})
    fl = False
    for i in range(5):
        if gsoup != None and len(gsoup) > 0:
            fl = True
            break
        fsoup = BeautifulSoup(driver.page_source,"html.parser")
        gsoup = fsoup.find_all("div",{"id":"search"})
    if gsoup == None or len(gsoup) < 1:
        gsoup = []
    else:
        gsoup = gsoup[0].find_all("div")
        if gsoup == None or len(gsoup) < 1:
            gsoup = []
        else:
            gsoup = gsoup[0].find_all("div")
            if gsoup == None or len(gsoup) < 1:
                gsoup = []
            else:
                gsoup = gsoup[0].contents
    if gsoup == None:
        gsoup = []
    for l_i in range(min(3,len(gsoup))):
        if not fl:
            break
        lsoup = gsoup[l_i].find_all("a",{"href":True})
        if lsoup == None or len(lsoup) < 1:
            continue
        li = lsoup[0].get("href")
        if li == None or not "http" in li or "huubr.com" in li:
            continue
        time.sleep(3)
        driver.get(li)
        redir_url = li # driver.current_url
        # print(redir_url)
        if redir_url[0:22] == "https://www.google.com":
            continue
        if redir_url[0:18] == "https://google.com":
            continue
        if "m.facebook" in redir_url:
            time.sleep(3)
            driver.get("facebook".join(redir_url.split("m.facebook")))
        psoup = fsoup
        fsoup = BeautifulSoup(driver.page_source,"html.parser")
        if redir_url[0:17] == "https://huubr.com" or redir_url[0:21] == "https://www.huubr.com":
            fsoup = fsoup.find_all("li",{"class":"business-email-id"})
            if fsoup != None and len(fsoup) > 0:
                fsoup = fsoup[0]
            else:
                fsoup = ''

        if fsoup != '':
            soup = fsoup.find_all("a")
        else:
            soup = []
        email = ''
        for i in soup:
            href = i.get('href')
            if href != None:
                if len(href) > 7:
                    if href[0:7] == 'mailto:':
                        email = href[7::]
                        break
        if email != '' and not "arifrayhan" in email and not "huubr.com" in email and not "yelp.com" in email and not "example" in email and not "myname" in email and not "bootstrap" in email and not ".co." in email and email[-3::].lower() != "png" and email[-3::].lower() != "jpg" and email[-4::].lower() != "webp" and email[-3::].lower() != ".js" and not email.split('@')[-1].split('.')[-1].isnumeric() and not "@." in email and '.' in email and email[0] != '?' and not "wixpress.com" in email and len(email.split('@')) > 1 and '.' in email.split('@')[1]:
            if email[0:3] == '%20':
                email = email[3::]
            write_csv([name,email,city])
            print('found:',name)
            print('email:',email)
            return 1
        elif redir_url[0:17] != "https://huubr.com" and redir_url[0:21] != "https://www.huubr.com":
            texts = str(fsoup).split()
            for lines in texts:
                parts = lines.split('@')
                if len(parts) > 1:
                    for j in range(1,len(parts)):
                        if '.' in parts[j] and len(parts[j]) > 2:
                            email = ''
                            for c in parts[j-1]:
                                if c.isalnum() or c == '-' or c == '_' or c == '.':
                                    email += c
                                else:
                                    email = ''
                            if email == '':
                                continue
                            email += '@'
                            for c in parts[j]:
                                if c.isalnum() or c == '-' or c == '.':
                                    email += c
                                else:
                                    break
                            if "arifrayhan" in email or "huubr.com" in email or "yelp.com" in email or "example" in email or "myname" in email or "bootstrap" in email or ".co." in email or email[-3::].lower() == "png" or email[-3::].lower() == "jpg" or email[-4::].lower() == "webp" or email[-3::].lower() == ".js" or email.split('@')[-1].split('.')[-1].isnumeric() or "@." in email or not '.' in email or email[0] == '?' or "wixpress.com" in email or len(email.split('@')) < 2 or not '.' in email.split('@')[1]:
                                continue
                            if email[0:3] == '%20':
                                email = email[3::]
                            write_csv([name,email,city])
                            fl = False
                            print('found:',name)
                            print('email:',email)
                            return 1
                if not fl:
                    break
        if psoup != fsoup:
            print('not found:',name)
    return 0

def main():

    global file_out

    # driver.get('https://www.google.com/')

    ct = datetime.datetime.now()

    timestr = time.strftime("%Y%m%d_%H%M%S")

    file_in = r'farhan.xlsx'

    # file_out = r'products_data_{0}.csv'.format(timestr)

    file_out = r'data.csv'

    df = pd.read_excel(file_in,engine='openpyxl')

    print('Total rows:',len(df))
    # exit()

    start_row = 2311
    cnt = 0

    for index, row in df.iterrows():
        if index < start_row:
            continue
        url = row.iloc[0]
        if len(url) < 1:
            continue
        try:
            if cnt == 57:
                break
            print(index+1,url)
            cnt += get_product_data(url,row.iloc[1])
            # return
        except Exception as e:
            print('Error:',str(e))
            # return
            # write_csv([url,f'Error: {str(e)}',"","","","","","","","","","","","","","","","","","","","",""])
            # write_csv([row.iloc[0],f'Not Found',row.iloc[1]])


        # input()
        # #test only
        # if index > 50:
        #     break
            
    
    print("End...")
    driver.quit()


if __name__ == '__main__':

    try:
        main()
        read_file = pd.read_csv(file_out,encoding='utf-8')
        read_file.to_excel(file_out.replace('.csv','')+'.xlsx', index=None, header=True)
        # os.remove(file_out)
    except Exception as e:
        # read_file = pd.read_csv(file_out,encoding='utf-8')
        # read_file.to_excel(file_out.replace('.csv','')+'.xlsx', index=None, header=True)
        # os.remove(file_out)
        print(e)

