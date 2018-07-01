import pprint

def clear_all_docs(self):
    all_docs = self._collection.find({})
    print("querried all docs, {num} found:".format(num=all_docs.count()))
    for doc in all_docs:
        # pprint.pprint(doc)
        self._collection.delete_one(doc)

def show_all_docs(self):
    pprint.pprint(self._collection.index_information())
    all_docs = self._collection.find({})
    print("querried all docs, {num} found:".format(num=all_docs.count()))
    for doc in all_docs:
        print("\t- " + doc["_id"] + ": " + doc['title'])
    print("\n")