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