from pymongo import MongoClient
import datetime

class Website:
    def __init__(self, homepage, scraper, collection):
        self._homepage = homepage
        self._scraper = scraper
        self._collection = collection

    def build_url_for_date(self, date, extra):
        return "{base}{path}?{key}={value}{end}".format(
            base=self._homepage,
            path=self.archive_url_path(),
            key=self.archive_url_key(),
            value=self.archive_url_value(date),
            end=self.archive_url_extra(extra)
        )

    def archive_url_path(self):
        raise NotImplementedError('subclasses must override archive_url_path()!')
    
    def archive_url_key(self):
        raise NotImplementedError('subclasses must override archive_url_key()!')

    def archive_url_value(self, date):
        raise NotImplementedError('subclasses must override archive_url_value()!')

    def archive_url_extra(self, data):
        raise NotImplementedError('subclasses must override archive_url_extra()!')


class SyriaHR(Website):

    def __init__(self, scraper, collection):
        Website.__init__(self, "http://www.syriahr.com/en/", scraper, collection)
        self._current_page = 1

    from .syriahr._get import get_article_urls_for_date
    from .syriahr._unique import check_if_unique
    # from .syriahr._parse import 
    from ._clear_docs import clear_all_docs, show_all_docs

    def archive_url_path(self):
        return ""
    
    def archive_url_key(self):
        return "m"

    def archive_url_value(self, date):
        return date.strftime("%Y%m")

    def archive_url_extra(self, extra):
        return "&paged={num}".format(num=extra)