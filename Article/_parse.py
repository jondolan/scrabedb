from bs4 import BeautifulSoup
import sys

def parse(self, html):
    article = BeautifulSoup(html, 'html.parser')
    
    try:
        self._title = article.find_all("h1", class_="post-title entry-title")[0].text
        self._body = article.find_all("div", class_="entry-content")[0].text
    except:
        print(html)
        print("Unexpected error:", sys.exc_info()[0])