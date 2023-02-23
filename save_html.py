import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import urllib.request

if __name__ == "__main__":
    i = 0
    with open(f"index.txt") as file:
        for line in file:
            url = line[3:]
           # r = requests.get(url).text
            html = urllib.request.urlopen(url).read().decode('utf-8')
            with open(f"output\{i}.html", 'w', encoding="utf-8") as output_file:
                output_file.write(html)
                output_file.close()
                i = i+1
