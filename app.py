from Article import Article
from Websites import SyriaHR
from pymongo import MongoClient, errors, TEXT
from datetime import datetime
import cfscrape
import os

if __name__ == "__main__":
    scraper = cfscrape.create_scraper()

    client = MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
    articles_db = client.articles
    syriahr = articles_db.syriahr

    site = SyriaHR(scraper, syriahr)
    # site.clear_all_docs()
    site.show_all_docs()
    syriahr.create_index([("body", TEXT), ("title", TEXT)], name='search_index', default_language='english')
    
    date = datetime.today()
    articles = site.get_article_urls_for_date(date)

    print("a total of {num} articles were found for {date}".format(
        num=len(articles),
        date=date))

    for article in articles:
        if (site.check_if_unique(article) == 1):
            print("Article {id} is unique, indexing!".format(id=article._uid))
            article.parse(scraper.get(article._url).content)
            syriahr.insert_one(article.export())
            # pprint.pprint(article.export())
        else:
            print("Search found a conflicting article for {id}".format(id=article._uid))



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