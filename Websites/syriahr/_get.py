from datetime import datetime
from bs4 import BeautifulSoup
from Article import Article

def get_article_urls_for_date(self, date):

    articles = []

    page_index = 1
    result = None
    while result != 0:
        url = self.build_url_for_date(date, page_index)
        print("Scraping for posts on page {url}".format(url=url))
        page = BeautifulSoup(self._scraper.get(url).content, 'html.parser')
        posts = page.find_all("li", class_="post-item")

        result = 0
        for post in posts:
            post_raw_date = post.find_all("span", class_="date meta-item")[0].find_all("span")[1].text
            post_date = datetime.strptime(post_raw_date, "%d/%m/%Y")
            # print("post_date: {post} - date: {compare} = {result}".format(
            #     post=post_date,
            #     compare=date,
            #     result=post_date-date.days
            # ))
            if abs((post_date-date).days) < 2:
                matched_post_url = post.find_all("a", class_="more-link")[0].get("href")
                # print("will index {posturl}".format(posturl=matched_post_url))
                uid = matched_post_url.split("=")[1]
                articles.append(Article(uid, matched_post_url, post_date))
                result += 1 
        page_index += 1

    # print("Stopped scrapping, found all for date {date}".format(date=date))
    return articles
    # result = scraper.get  


    # for i in range(1, 79):
    #     print(self.build_url_for_date(date, i))