import requests
import xml.etree.ElementTree as ET
import gspread
from bs4 import BeautifulSoup

sitemap_url = input('What is the sitemap URL of your website? \n')

gc = gspread.service_account(filename="api.json")