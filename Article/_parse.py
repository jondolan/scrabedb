from bs4 import BeautifulSoup

def parse(self, html):
    article = BeautifulSoup(html, 'html.parser')
    
    self._title = article.find_all("h1", class_="post-title entry-title")[0].text
    self._body = article.find_all("div", class_="entry-content")[0].text