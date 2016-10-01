#Web Crawler for receiving RSS/Atom feeds
import feedparser
from couchdb import Server
import os
import hashlib
from uuid import uuid4

feedurls = []
feedurls += [r'./test/example.xml']
feedurls += ['http://www.heise.de/newsticker/heise-atom.xml']

itemstorage = []

class Feed(object):
    items = []
    def __init__(self, parsedfeed):
        self.title = parsedfeed.feed.get('title','')
        self.link = parsedfeed.feed.get('link','')
        self.subtitle = parsedfeed.feed.get('subtitle','')

class Item(object):
    def __init__(self, item_dict, feed):
        try:
            self.title = str(item_dict['title'])
        except:
            self.title = ""
        try:
            self.link = str(item_dict['link'])
        except:
            self.link = ""
        try:
            self.id = str(item_dict['id'])
        except:
            self.id = str(hashlib.sha256(self.link.encode('ASCII')).hexdigest())

        try:
            self.published = (item_dict['published'])
        except:
            self.published = ""
        try:
            self.updated = str(item_dict['updated'])
        except:
            self.updated = ""
        try:
            self.summary = str(item_dict['summary'])
        except:
            self.summary = ""
        try:
            self.content = str(item_dict['content'])
        except:
            self.content = ""
        self.feed = { 'title': feed.title, 'link': feed.link, 'subtitle':
                feed.subtitle}
    def to_dict(self):
        return {
                '_id': uuid4().hex,
                'type': 'item',
                'schemaversion': 1,
                'title': self.title,
                'link': self.link,
                'id': self.id,
                'published': self.published,
                'updated': self.updated,
                'summary': self.summary,
                'content':  self.content
                }

if __name__ == "__main__":
    server = Server(os.environ['COUCHURL'])
    database = server['simdata']

    print("database name: " + database.name)
    for url in feedurls:
        parsedfeed = feedparser.parse(url)
        print(parsedfeed.feed.title)
        feed = Feed(parsedfeed)
        for entry in parsedfeed.entries:
            itm = Item(entry, feed)
            itemstorage += [itm]

    for i in itemstorage:
        database.save(i.to_dict())


