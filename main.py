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

def scrape_url(url, worksheet):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    row = [url]

    ## is there title tag?
    title_tag = soup.find('title')
    if title_tag:
        row.append("yes")
    else:
        row.append("no")
    
    ## are there meta tags?
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if tag.get('name') == 'description':
            row.append("yes")
            break
        else:
            row.append("no")

    ## are there h1 tags?
    h1_tags = soup.find('h1')
    if h1_tags:
        row.append("yes")
    else:
        row.append("no")

    # are there h2 tags?
    h2_tags = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
    if h2_tags:
        row.append("yes")
    else:
        row.append("no")

    worksheet.append_row(row)

#function to scrape all URLs in the sitemap and its sub-sitemaps

def scrape_sitemap(sitemap_url, worksheet):
    response = requests.get(sitemap_url)
    sitemap_content = response.text
    sitemap_xml = ET.fromstring(sitemap_content)

    for element in sitemap_xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        alt_sitemap_url = element.text
        scrape_sitemap(alt_sitemap_url, worksheet)

    for element in sitemap_xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        url = element.text
        scrape_url(url, worksheet)



