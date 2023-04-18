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

# create the table and headers
headers = ["URL", "Title Tags", "Meta Description", "H1 Tags", "H2-H6 Tags", "Breadcrumbs", "Internal Linking", "Structured Data", "Social Media Tags", "Canonical URLs" "Www Vs. Non-www", "Http:// vs Https://", "Proper HTTP Status Code"]
header_range = "A1:N1"
worksheet.update(header_range, [headers])
worksheet.format(header_range, {"horizontalAlignment": "Center", "textFormat": {"bold": True}})


