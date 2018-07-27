from Article import Article
from Websites import SyriaHR
from pymongo import MongoClient, errors, TEXT
from datetime import datetime, timedelta
import calendar
import cfscrape
import os
from threading import Thread
from sys import stdout

def end_of_month(start):
    last_day = calendar.monthrange(start.year, start.month)
    return start.replace(day=last_day[1])

def next_month(start):
    tmp1 = start.replace(day=1)
    tmp2 = tmp1 + timedelta(days=32)
    return tmp2.replace(day=1)

if __name__ == "__main__":
    # start_date = datetime(2014, 1, 1)
    start_date = datetime.strptime(os.environ['SCRAPER_START_DATE'], "%Y-%m-%d")
    end_date = datetime.now()

    scraper = cfscrape.create_scraper()

    client = MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
    articles_db = client.articles
    syriahr = articles_db.syriahr

    site = SyriaHR(scraper, syriahr)
    # site.clear_all_docs()
    # site.show_all_docs()
    print("There are {num} articles currently in the database".format(num=site.how_many_docs()))
    syriahr.create_index([("body", TEXT), ("title", TEXT)], name='search_index', default_language='english')

    current_date = start_date
    print("Scraper started for {start} to {end}".format(start=start_date, end=end_date))
    while current_date < end_date:

    # for i in range(0, len(dates)-1):
        # start_date = dates[i]
        # end_date = dates[i+1]

        current_end_date = end_of_month(current_date)
        if current_end_date > end_date:
            current_end_date = end_date

        print("\tfinding from {start} to {end}".format(start=current_date, end=current_end_date))

        try:
            articles = site.get_article_urls_for_date_range(current_date, current_end_date)

            print("\ta total of {num} articles were found for range from {start_date} to {end_date}".format(
                num=len(articles),
                start_date=current_date,
                end_date=current_end_date))

            for article in articles:
                if (site.check_if_unique(article) == 1):
                    print("\t\tArticle {id} is new, adding to database!".format(id=article._uid))
                    article.parse(scraper.get(article._url).content)
                    syriahr.insert_one(article.export())
                    # pprint.pprint(article.export())
                else:
                    print("\t\tAlready indexed article {id}".format(id=article._uid))
                stdout.flush()
        except:
            print("Failed big time:", sys.exc_info()[0])
            
        current_date = next_month(current_date)