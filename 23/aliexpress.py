import os
def pre():
    os.system("pip install selenium==4.12.0")
    os.system("pip install undetected-chromedriver==3.5.3")
    os.system("pip install pandas==2.1.2")
    os.system("pip install chromedriver_autoinstaller==0.6.2")
    os.system("pip install beautifulsoup4==4.12.2")
    os.system("pip install openpyxl==3.1.2")
if  not os.path.isfile("pre"):
    pre()
    f = open("pre","w")
    f.close()

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
        headers = ['Aliexpress URL','Redirected URL','Status','Product Name','Variant Name (Default)','Variant Value (Default)','Variant Name2','Variant Value2','Variant Name3','Variant Value3','Price $NZD (Default)','Shipping $NZD (Default)','Shipping Method (Default)','Shipping2 $NZD','Shipping Method2','Shipping3 $NZD','Shipping Method3',	'Sold Number','Rating','Reviews','Category','Store Name',	'Store Rating']
        writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
        if not csv_exist:
            writer.writerow(headers)

        writer.writerow(data)

def get_product_data(url):
    
    driver.get(url)

    data_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//script[contains(text(),"window.runParams")]')
            )
        ).get_attribute('innerHTML').strip()
    
    # print(data_text)
    
    data_match = re.search('data: ({.+?})\n', data_text)

    # print(data_match)

    if data_match:


        try:
            status = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class,"message--wrap--")]')
                )
            ).text.strip()

        except Exception as e:
            print('error status')
            status = ''


        try:
            soup = BeautifulSoup(driver.page_source,"html.parser")
            fsoup = []
            for div in soup.find_all("div",{"class":True}):
                if "sku-item--property" in ''.join(div.get("class")):
                    fsoup.append(div)
            variant = [0]*len(fsoup)
            for i in range(len(fsoup)):
                skus = fsoup[i].find_all("div",{"data-sku-col":True})
                variant[i] = [0]*(len(skus)+1)
                variant[i][0] = fsoup[i].find("div").text.split(":")[0].strip()
                for j in range(1,len(skus)+1):
                    for k in skus[j-1].find_all("img"):
                        variant[i][j] = k.get("alt")
                    if variant[i][j] == 0:
                        variant[i][j] = skus[j-1].find("span").text
            
            if len(variant) < 1:
                variant_name = ""
                variant_value = [""]
                variant_name2 = ""
                variant_value2 = [""]
                variant_name3 = ""
                variant_value3 = [""]
            elif len(variant) == 1:
                variant_name = variant[0][0]
                variant_value = variant[0][1::]
                variant_name2 = ""
                variant_value2 = [""]
                variant_name3 = ""
                variant_value3 = [""]
            elif len(variant) == 2:
                variant_name = variant[0][0]
                variant_value = variant[0][1::]
                variant_name2 = variant[1][0]
                variant_value2 = variant[1][1::]
                variant_name3 = ""
                variant_value3 = [""]
            elif len(variant) > 2:
                variant_name = variant[0][0]
                variant_value = variant[0][1::]
                variant_name2 = variant[1][0]
                variant_value2 = variant[1][1::]
                variant_name3 = variant[2][0]
                variant_value3 = variant[2][1::]

            # variant_name_value = WebDriverWait(driver, 2).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//div[contains(@class,"sku-item--property")]//span')
            #     )
            # ).text.strip()

            # variant_split = variant_name_value.split(':')

            # variant_name = variant_split[0]
            # variant_value = variant_split[1]


        except Exception as e:
            print('error variant name,value')
            variant_name = ''
            variant_value = []
            
        data = json.loads(data_match.group(1))
        product_name = get_value(data,"['productInfoComponent']['subject']")
        # variant_name = get_value(data,"['skuComponent']['productSKUPropertyList'][0]['skuPropertyValues'][0]['propertyValueDisplayName']")
        # price = get_value(data,"['priceComponent']['discountPrice']['minActivityAmount']['value']")
        try:      
            pricet = get_value(data,"['metaDataComponent']['ogTitle']")
            price = ""
            f = True
            for c in pricet:
                if c.isnumeric():
                    f=False
                    price += c
                elif c == '.' and not f:
                    price += c
                elif c != ',' and not f:
                    break
            if f:
                price = ''.join(pricet.split())
        except Exception as e:
            print('error price')
        
        shippings = []
        try:
            soup = BeautifulSoup(driver.page_source,"html.parser")
            fsoup = []
            shipping_name = ""
            shipping_value = ""
            for div in soup.find_all("div",{"class":"dynamic-shipping-line"}):
                if "shipping" in div.text.lower():
                    fsoup.append(div)
                else:
                    shipping_value = "".join(div.text.split())
                break
            
            if len(fsoup) > 0:
                f = True
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(@class,"shipping--wrap--")]')
                        )
                    ).click()
                except:
                    f=False
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//button[contains(@class,"logistics--moreOptions--")]')
                        )
                    ).click()
                except:
                    pass
                if f:
                    soup = BeautifulSoup(driver.page_source,"html.parser")
                    fsoup = soup.find_all("div",{"class":"comet-v2-modal"})
                    # print(str(fsoup))
                    for fsoup in fsoup:
                        fsoup = fsoup.find_all("div",{"class":"dynamic-shipping"})
                        shippings = [0]*len(fsoup)
                        for i in range(len(fsoup)):
                            fsoupi = fsoup[i].find_all("div",{"class":"dynamic-shipping-line"})
                            shippings[i] = [0,""]
                            shippings[i][0] = ''.join(fsoupi[2].text.split())+" | "+''.join(fsoupi[3].text.split())
                            f = True
                            for c in fsoupi[0].text:
                                if c.isnumeric():
                                    f=False
                                    shippings[i][1] += c
                                elif c == '.' and not f:
                                    shippings[i][1] += c
                                elif c != ',' and not f:
                                    break
                            if f:
                                shippings[i][1] = ''.join(fsoupi[0].text.split())
            
            if len(shippings) < 1:
                shipping_name = ""
                shipping_value = ""
                shipping_name2 = ""
                shipping_value2 = ""
                shipping_name3 = ""
                shipping_value3 = ""
            elif len(shippings) == 1:
                shipping_name = shippings[0][0]
                shipping_value = shippings[0][1]
                shipping_name2 = ""
                shipping_value2 = ""
                shipping_name3 = ""
                shipping_value3 = ""
            elif len(shippings) == 2:
                shipping_name = shippings[0][0]
                shipping_value = shippings[0][1]
                shipping_name2 = shippings[1][0]
                shipping_value2 = shippings[1][1]
                shipping_name3 = ""
                shipping_value3 = ""
            elif len(shippings) > 2:
                shipping_name = shippings[0][0]
                shipping_value = shippings[0][1]
                shipping_name2 = shippings[1][0]
                shipping_value2 = shippings[1][1]
                shipping_name3 = shippings[2][0]
                shipping_value3 = shippings[2][1]



        except Exception as e:
            print('error shipping name,value')
            print(e)
            shipping_name = ''
            shipping_value = ''


        sold_number = get_value(data,"['tradeComponent']['formatTradeCount']")

        rating = get_value(data,"['feedbackComponent']['evarageStar']")

        reviews =  get_value(data,"['feedbackComponent']['totalValidNum']")


        category_list = get_value(data,"['breadcrumbComponent']['pathList']")
        category = []
        if category_list:
            for i,c in enumerate(category_list):
                if i <= 1:
                    continue
                category.append(c['name'])
        else:
            category = ''
        
        if isinstance(category,list):
             category = ', '.join(category)
        
        store_name =  get_value(data,"['sellerComponent']['storeName']")
        store_rating = get_value(data,"['storeFeedbackComponent']['sellerPositiveRate']") 

        redir_url = driver.current_url

        ln3 = len(variant_value3)
        if not ln3:
            ln3 = 1
        ln2 = len(variant_value2)
        if not ln2:
            ln2 = 1
        ln = len(variant_value)
        if not ln:
            ln = 1
        for i in variant_value3:
            for j in variant_value2:
                for k in variant_value:
                    print(url,redir_url,status,product_name,variant_name,k,variant_name2,j,variant_name3,i,price,shipping_value,shipping_name,shipping_value2,shipping_name2,shipping_value3,shipping_name3,sold_number,rating,reviews,category,store_name,store_rating)
                    write_csv([url,redir_url,status,product_name,variant_name,k,variant_name2,j,variant_name3,i,price,shipping_value,shipping_name,shipping_value2,shipping_name2,shipping_value3,shipping_name3,sold_number,rating,reviews,category,store_name,store_rating])
    else:

        try:
            status = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[contains(@class,"item-not-found-notice")]')
                )
            ).text.strip()

            # print(url,status,"","","","","","","","","","","","")
            write_csv([url,status,"","","","","","","","","","","","","","","","","","","",""])

        except Exception as e:
            print('error status')
            status = ''
            write_csv([url,"Unknown","","","","","","","","","","","","","","","","","","","",""])

def login(usr,pas):
    if len(usr.split("@")) != 2:
        print("Invalid username")
        return
    cr_usr = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[contains(@class,"my-account--small--")]')
        )
    ).get_attribute('innerText')
    if len(cr_usr.split(",")) > 1 and cr_usr.split(",")[1].strip() == usr.split("@")[0]:
        print("Already logged in user:",cr_usr.split(",")[1].strip())
        return
    if len(cr_usr.split(",")) > 1:
        print("Loging out user:",cr_usr.split(",")[1].strip())
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(@class,"my-account--centerIcon--")]')
            )
        ).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(@class,"my-account--out--")]')
            )
        ).click()
    print("Attempting login user:",usr)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(@class,"lgh-contain-login-btn")]')
        )
    ).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//input[contains(@id,"fm-login-id")]')
        )
    ).send_keys(usr)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//input[contains(@id,"fm-login-password")]')
        )
    ).send_keys(pas)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@class,"login-submit")]')
        )
    ).click()
    cr_usr = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[contains(@class,"my-account--small--")]')
        )
    ).get_attribute('innerText')
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class,"email-header-title")]')
            )
        ).click()
        msgbox('Just enter the verification code manually within 60 second. Then everything will work automatically')
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class,"comet-btn")]')
            )
        ).click()
    except:
        pass
    print("done")
    time.sleep(20)

def main():

    global file_out

    driver.get('https://www.aliexpress.com/')

    # msgbox('be sure to select Ship To, Language and Currency before continue. :)')
    if  os.path.isfile("id.txt"):
        f = open("id.txt","r")
        usr = f.readlines()
        f.close()
        pas = usr[1].strip()
        usr = usr[0].strip()
        login(usr,pas)

    ct = datetime.datetime.now()

    timestr = time.strftime("%Y%m%d_%H%M%S")

    file_in = r'products.xlsx'

    file_out = r'products_data_{0}.csv'.format(timestr)

    df = pd.read_excel(file_in,engine='openpyxl')

    print('Total rows:',len(df))
    # exit()

    start_row = 0

    for index, row in df.iterrows():
        url = row.iloc[0]
        print(index,url)

        if pd.isnull(url) or pd.isna(url):
            print('skitp url is nan or null',index,url)
            continue

        if index < start_row:
            print('skip row:',index,url)
            continue

        if not uri_validator(url):
            print('skip invalid url:',index,url)
            continue
        
        try:
            get_product_data(url)
        except Exception as e:
            print('Error:',str(e))
            write_csv([url,f'Error: {str(e)}',"","","","","","","","","","","","","","","","","","","","",""])


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
        os.remove(file_out)
    except Exception as e:
        read_file = pd.read_csv(file_out,encoding='utf-8')
        read_file.to_excel(file_out.replace('.csv','')+'.xlsx', index=None, header=True)
        os.remove(file_out)
        print(e)

