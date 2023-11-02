import datetime
import os
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
from webdriver_manager.chrome import ChromeDriverManager
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


driver_path = ChromeDriverManager().install()

# driver_path = r'C:\Users\Danysys\.wdm\drivers\chromedriver\win64\116.0.5845.111\chromedriver-win32/chromedriver.exe'

print(driver_path)

options = uc.ChromeOptions()
# options.headless = True
# options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={application_path}\seleniumdata")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--log-level=3")
options.add_argument("--no-first-run")
# options.add_argument("--disable-single-click-autofill")

driver = uc.Chrome(Service=ChromeDriverManager().install(),options=options)

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
        headers = ['Aliexpress URL','Status','Product Name','Variant Name (Default)','Variant Value (Default)','Price $NZD (Default)','Shipping $NZD (Default)','Shipping Method (Default)',	'Sold Number','Rating','Reviews','Category','Store Name',	'Store Rating']
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
            variant_name_value = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class,"sku-item--property")]//span')
                )
            ).text.strip()

            variant_split = variant_name_value.split(':')

            variant_name = variant_split[0]
            variant_value = variant_split[1]


        except Exception as e:
            print('error variant name,value')
            variant_name = ''
            variant_value = ''

        # try:
        #     variant_value = WebDriverWait(driver, 2).until(
        #         EC.presence_of_element_located(
        #             (By.XPATH, '//div[contains(@class,"sku-item--property")]//span/span')
        #         )
        #     ).text.strip()
        # except Exception as e:
        #     print('error variant value')
        #     variant_value = ''

            
        data = json.loads(data_match.group(1))
        product_name = get_value(data,"['productInfoComponent']['subject']")
        # variant_name = get_value(data,"['skuComponent']['productSKUPropertyList'][0]['skuPropertyValues'][0]['propertyValueDisplayName']")
        # price = get_value(data,"['priceComponent']['discountPrice']['minActivityAmount']['value']")
        try:      
            price = get_value(data,"['metaDataComponent']['ogTitle']").split('NZ$')[0]
        except Exception as e:
            print('error price')
        
        shipping = get_value(data,"['webGeneralFreightCalculateComponent']['originalLayoutResultList'][0]['bizData']")

        if shipping:
            shipping_free = get_value(shipping,"['shippingFee']")
            # print(shipping_free)
            if shipping_free:
                if shipping_free.lower() == 'free':
                    shipping = shipping_free
                else:
                    shipping = get_value(shipping,"['displayAmount']")
            else:
                shipping = "This product can't be shipped to your address"
        else:
            shipping = ''

        shipping_method = get_value(data,"['webGeneralFreightCalculateComponent']['originalLayoutResultList'][0]['bizData']['deliveryProviderName']")

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

        print(url,status,product_name,variant_name,variant_value,price,shipping,shipping_method,sold_number,rating,reviews,category,store_name,store_rating)
        write_csv([url,status,product_name,variant_name,variant_value,price,shipping,shipping_method,sold_number,rating,reviews,category,store_name,store_rating])
    else:

        try:
            status = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[contains(@class,"item-not-found-notice")]')
                )
            ).text.strip()

            # print(url,status,"","","","","","","","","","","","")
            write_csv([url,status,"","","","","","","","","","",""])

        except Exception as e:
            print('error status')
            status = ''
            write_csv([url,"Unknown","","","","","","","","","","",""])

def login(usr,pas):
    print("Attempting login user:",usr)
    sign_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class,"my-account--signin--")]')
                )
            )
    sign_button.click()
    time.sleep(20)
    pass

def main():

    global file_out

    driver.get('https://www.aliexpress.com/')

    # msgbox('be sure to select Ship To, Language and Currency before continue. :)')

    login("arifrayhan54@gmail.com","testpass")

    ct = datetime.datetime.now()

    timestr = time.strftime("%Y%m%d_%H%M%S")

    file_in = r'products.xlsx'

    file_out = r'products_data_{0}.csv'.format(timestr)

    df = pd.read_excel(file_in,engine='openpyxl')

    print('Total rows:',len(df))
    # exit()

    start_row = 0

    for index, row in df.iterrows():
        url = row[0]
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
            write_csv([url,f'Error: {str(e)}',"","","","","","","","","","","",""])


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

