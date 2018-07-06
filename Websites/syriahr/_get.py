import datetime
from bs4 import BeautifulSoup
from Article import Article


def get_article_urls_for_date_range(self, start_date, end_date):

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)

    articles = []

    date_for_url = start_date
    page_index = 1

    while start_date <= date_for_url <= end_date:
        url = self.build_url_for_date(date_for_url, page_index)
        print("Scraping for posts on page {url}".format(url=url))
        page = BeautifulSoup(self._scraper.get(url).content, 'html.parser')
        posts = page.find_all("li", class_="post-item")

        # print(len(posts))
        if len(posts) == 0:
            date_for_url = add_one_month(date_for_url)
            page_index = 1
        else:
            for post in posts:
                post_raw_date = post.find_all("span", class_="date meta-item")[0].find_all("span")[1].text
                post_date = datetime.datetime.strptime(post_raw_date, "%d/%m/%Y")
                
                # print(start_date)
                # print(post_date)
                # print(end_date)

                if start_date <= post_date <= end_date:
                    matched_post_url = post.find_all("a", class_="more-link")[0].get("href")
                    # print("will index {posturl}".format(posturl=matched_post_url))
                    uid = matched_post_url.split("=")[1]
                    articles.append(Article(uid, matched_post_url, post_date))
            page_index += 1

    # print("Stopped scrapping, found all for date {date}".format(date=date))
    return articles
    # result = scraper.get  


    # for i in range(1, 79):
    #     print(self.build_url_for_date(date, i))


def add_one_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 =  dt1 + datetime.timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3