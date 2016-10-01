#Web Crawler for receiving RSS/Atom feeds
import feedparser
from couchdb import Server
import os
import hashlib
from uuid import uuid4


itemstorage = []

class Feed(object):
    items = []
    def __init__(self, feedinfo ):
        self.title = feedinfo.value.get('title', 'No title')#['value']['title']
        self.url = feedinfo.value.get('url', '')
        self.name = feedinfo.value.get('name', '')
        self.id = feedinfo.value.get('_id', 'yee')
    def update_info(self, feedinfo):
        if feedinfo.title is not self.title:
            self.title = feedinfo.title

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
        self.feed = { 'title': feed.title, 'url': feed.url, 'name':
                feed.name, 'id': feed.id}
    def to_dict(self):
        return {
                '_id': uuid4().hex,
                'type': 'item',
                'schemaversion': 1,
                'feedId': self.feed['id'],
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
    feedlist = []
    for row in database.view("all/if_feed"):
        feedlist += [Feed(row)]

    print("database name: " + database.name)

    for feed in feedlist:
        parsedfeed = feedparser.parse(feed.url)
        print(feed.title)
        #feed.update_info(parsedfeed)

        for entry in parsedfeed.entries:
            itm = Item(entry, feed)
            itemstorage += [itm]

#    for i in itemstorage:
#        database.save(i.to_dict())
    

