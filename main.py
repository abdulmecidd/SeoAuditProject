import requests
import xml.etree.ElementTree as ET
import gspread
from bs4 import BeautifulSoup

sitemap_url = input('What is the sitemap URL of your website? \n')

gc = gspread.service_account(filename="api.json")
sh_name = input("What is the name of the worksheet you want to create? \n")

# create or open a worksheet with the specific name
try: 
    sh = gc.open(sh_name)
    worksheet = sh.sheet1
except gspread.exceptions.SpreadsheetNotFound:
    sh = gc.create(sh_name)
    worksheet = sh.sheet1

