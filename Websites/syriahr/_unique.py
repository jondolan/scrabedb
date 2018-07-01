def check_if_unique(self, article):
    search = self._collection.find_one({"_id": article._uid})
    if (search == None):
        return 1
    else:
        return 0