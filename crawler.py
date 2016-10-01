#Web Crawler for receiving RSS/Atom feeds
import feedparser
from couchdb import Server
import os
from feed import Feed
from item import Item


itemstorage = []

if __name__ == "__main__":
    server = Server(os.environ['COUCHURL'])
    database = server['simdata']
    feedlist = []
    map_if_feed = '''
function(doc) {

    if( doc.type == "feed" ){
        emit( doc.type , doc);
    }

}
'''

    for row in database.query(map_if_feed):
        feedlist += [Feed(row)]

    print("database name: " + database.name)

    for feed in feedlist:
        parsedfeed = feedparser.parse(feed.url)
        print(feed.title)
        #feed.update_info(parsedfeed)

        for entry in parsedfeed.entries:
            itm = Item(entry, feed)
            itemstorage += [itm]

    for i in itemstorage:
        database.save(i.to_dict())
