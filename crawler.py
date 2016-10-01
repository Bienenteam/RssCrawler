#Web Crawler for receiving RSS/Atom feeds
import feedparser
from couchdb import Server
import os
import hashlib
from uuid import uuid4
from feed import Feed
from item import Item


itemstorage = []

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
