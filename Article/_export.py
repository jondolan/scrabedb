import datetime

def export(self):
	return {"_id": self._uid,
			"url": self._url,
			"date": self._date,
			"title": self._title,
			"body": self._body}