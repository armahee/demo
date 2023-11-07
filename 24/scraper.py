import os
import sys
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

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
gdrive = GoogleDrive(gauth) 

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
df_name = "data-"+str(t_i+1)+".csv"
if  not os.path.isfile(application_path+"/data/data-"+str(t_i+1)+".csv"):
    f = open(application_path+"/data/data.csv","w")
    f.write("SL,EAN CODE,DESCRIPTION,DETAIL DESCRIPTION,PVP,PVP /UNIT,STOCK,picture with the EAN title\n")
    f.close()
f_name = application_path+"/data/data-"+str(t_i+1)+".csv"
f = open(f_name, "a")
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
    # time.sleep(60)
    # exit()
    print("scraping")
    try:
        soup = BeautifulSoup(driver.page_source,"html.parser")
        skus = soup.find_all("script",{"type":"application/ld+json"})
        sku = ""
        for a in skus:
            inh = a.get_text().split(',')
            for b in inh:
                if b[0:5] == '"sku"':
                    b = b.split(':')
                    if len(b) > 1:
                        sku = b[1]
                    break
        descs = soup.find_all("h1",{"class":"pdp-product-name"})
        des = ""
        for a in descs:
            inh = ' '.join(a.get_text().split())
            inh = "'".join(inh.split('"'))
            des = '"'+inh+'"'
        ddescs = soup.find_all("div",{"class":"pdp-description-content"})
        ddes = ""
        for a in ddescs:
            inh = ' '.join(str(a).split())
            inh = "'".join(inh.split('"'))
            ddes = '"'+inh+'"'
            break
        prcs = soup.find_all("span",{"data-item-price":True})
        prc = ""
        for a in prcs:
            inh = ''.join(a.get("data-item-price").split())
            inh = "'".join(inh.split('"'))
            prc = '"'+inh+'"'
            break
        uprcs = soup.find_all("span",{"class":"unit-info"})
        uprc = ""
        for a in uprcs:
            inh = ''.join(a.get_text().split())
            inh = "'".join(inh.split('"'))
            uprc = '"'+inh+'"'
            break
        stocks = soup.find_all("script",{"type":"text/javascript"})
        stock = ""
        for a in stocks:
            inh = a.get_text().split(',')
            for b in inh:
                if b[0:10] == '"IN_STOCK"':
                    b = b.split(':')
                    if len(b) > 1:
                        stock = b[1]
                    break
        imgs = soup.find_all("script",{"type":"application/ld+json"})
        img = ""
        for a in imgs:
            inh = a.get_text().split(',')
            for b in inh:
                if b[0:7] == '"image"':
                    b = b.split(':')
                    if len(b) > 2:
                        b = b[2]
                        img = b.split('"')[0]
                        img = "'".join(img.split('"'))
                        img = '"https:'+img+'"'
                    break
        cnt = ""
        if len(sku) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(des) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(ddes) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(prc) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(uprc) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(stock) > 0:
            cnt += "1"
        else:
            cnt += "0"
        if len(img) > 0:
            cnt += "1"
        else:
            cnt += "0"

        f.write(str(t_i)+","+sku+","+des+","+ddes+","+prc+","+uprc+","+stock+","+img+"\n")
        f.flush()
        print(t_i,":",cnt)

    except Exception as e:
        print('error scraping')
        print(e)
    print("ok")

f.close()

path = application_path+"/data"
x = df_name
df = gdrive.CreateFile({'title': x}) 
df.SetContentFile(os.path.join(path, x)) 
df.Upload() 
df = None
