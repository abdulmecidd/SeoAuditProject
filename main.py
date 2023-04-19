import requests
import xml.etree.ElementTree as ET
import gspread
from bs4 import BeautifulSoup
from urllib.parse import urlparse

sitemap_url = input('What is the sitemap URL of your website? \n')

if not sitemap_url:
    print("Please entry a value\n")
else:

    gc = gspread.service_account(filename="api.json")
    sh_name = input("What is the name of the worksheet you want to create? \n")
    if sh_name:
        # create or open a worksheet with the specific name
        try: 
            sh = gc.open(sh_name)
            worksheet = sh.sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            sh = gc.create(sh_name)
            worksheet = sh.sheet1

        # create the table and headers
        headers = ["URL", "Title Tags", "Meta Description", "H1 Tags", "H2-H6 Tags", "Internal Linking", "Social Media Tags", "Canonical URLs" "Www Vs. Non-www", "Http:// vs Https://", "Proper HTTP Status Code"]
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

            meta_tags = soup.find_all("meta")

            if meta_tags:
                row.append("yes")
            else:
                row.append("no")
            
            h1_tags = soup.find('h1')

            if h1_tags:
                row.append("yes")
            else:
                row.append('no')

            h2h3_tags = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])

            if h2h3_tags:
                row.append("yes")
            else:
                row.append("no")

            internalLinks = soup.find_all('a')
            if internalLinks:
                row.append("yes")
            else:
                row.append("no")

            for tag in meta_tags:
                if tag.get('property') == 'og:title' or tag.get('property') == 'og:image':
                    row.append("yes")
                    break
            
            row.append('no') if len(row) == 1 else None    

            parsed_url = urlparse(url)
            
            if parsed_url.netloc.startswith("www."):
                row.append("www")
            else:
                row.append("None www")
            
            if parsed_url.scheme.startswith("https"):
                row.append("https://")
            else:
                row.append("http://")

            row.append(response.status_code)

            worksheet.append_row(row)
            print(row)
            print(parsed_url)

        #function to scrape all URLs in the sitemap and its sub-sitemaps

        def scrape_sitemap(sitemap_url, worksheet):
            response = requests.get(sitemap_url)
            sitemap_content = response.text
            sitemap_xml = ET.fromstring(sitemap_content)

            for element in sitemap_xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                alt_sitemap_url = element.text
                scrape_sitemap(alt_sitemap_url, worksheet)

            for element in sitemap_xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = element.text
                scrape_url(url, worksheet)

        #call the function to start scraping

        scrape_sitemap(sitemap_url, worksheet)

        print("scraping is complete!")
    else:
        print("Please entry a value!")
