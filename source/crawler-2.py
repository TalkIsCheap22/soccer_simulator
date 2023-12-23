from bs4 import BeautifulSoup
import urllib.request

url = "https://1x2stats.com/en-gb/ENG/2022/Premier-League/"
html = urllib.request.urlopen(url).read().decode('utf-8')
