from Article import Article
from Websites import SyriaHR
from pymongo import MongoClient, errors, TEXT
from datetime import datetime, timedelta
import calendar
import cfscrape
import os

def end_of_month(start):
    last_day = calendar.monthrange(start.year, start.month)
    return start.replace(day=last_day[1])

def next_month(start):
    tmp1 = start.replace(day=1)
    tmp2 = tmp1 + timedelta(days=32)
    return tmp2.replace(day=1)

if __name__ == "__main__":
    scraper = cfscrape.create_scraper()

    client = MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
    articles_db = client.articles
    syriahr = articles_db.syriahr

    site = SyriaHR(scraper, syriahr)
    # site.clear_all_docs()
    # site.show_all_docs()
    print("There are {num} articles currently in the database".format(num=site.how_many_docs()))
    syriahr.create_index([("body", TEXT), ("title", TEXT)], name='search_index', default_language='english')

    start_date = datetime(2012, 1, 1)
    end_date = datetime.now()

    current_date = start_date
    while current_date < end_date:

    # for i in range(0, len(dates)-1):
        # start_date = dates[i]
        # end_date = dates[i+1]

        current_end_date = end_of_month(current_date)
        if current_end_date > end_date:
            current_end_date = end_date

        print("Finding from {start} to {end}".format(start=current_date, end=current_end_date))

        articles = site.get_article_urls_for_date_range(current_date, current_end_date)

        print("a total of {num} articles were found for range from {start_date} to {end_date}".format(
            num=len(articles),
            start_date=current_date,
            end_date=current_end_date))

        for article in articles:
            if (site.check_if_unique(article) == 1):
                print("Article {id} is new, adding to database!".format(id=article._uid))
                article.parse(scraper.get(article._url).content)
                syriahr.insert_one(article.export())
                # pprint.pprint(article.export())
            else:
                print("Already indexed article {id}".format(id=article._uid))

        current_date = next_month(current_date)

# print("inserting test article")
    # inserted_id = syriahr.insert_one(Article.test_article().export()).inserted_id
    # print("querying for test article")
    # find = syriahr.find_one({"_id": inserted_id})
    # print("printing found test article")
    # pprint.pprint(find)

    # try:
    #     print("inserting test article AGAIN")
    #     failed_insert = syriahr.insert_one(Article.test_article().export()).inserted_id
    # except errors.DuplicateKeyError:
    #     print("...which failed, duplicate key error")

    # print("deleting test article")
    # syriahr.delete_one(find)
    
    # all_docs = syriahr.find({})
    # print("querried all docs, {num} found".format(num=all_docs.count()))
    # for doc in all_docs:
    #     pprint.pprint(doc)
    #     syriahr.delete_one(doc)