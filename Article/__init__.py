from datetime import datetime

class Article:

    def __init__(self, uid, url, date, title=None, body=None):
        self._uid = uid
        self._url = url
        self._date = date
        self._title = title
        self._body = body

    from ._export import export
    from ._parse import parse
    from ._dump import dump_collection

    @staticmethod
    def test_article():
        return Article(69, "http://jonpdolan.com", datetime.now(), "Test article", "This is the fake content of a fake article! Hope you enjoyed!")
        # print(article.export())
        # collection.insert_one(article.export())