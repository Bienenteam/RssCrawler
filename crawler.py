#Web Crawler for receiving RSS/Atom feeds
import feedparser
import couchdb
from couchdb import Server
import os
from feed import Feed
from item import Item


itemstorage = []

if __name__ == "__main__":
    server = Server(os.environ['COUCHURL'])
    database = server['beehive']
    feedlist = []
    map_if_feed = '''
function(doc) {

    if( doc.type == "feed" ){
        emit( doc.type , doc);
    }

}
'''
    map_if_key_is_known = '''
function(doc) {
    if (doc.type === 'item') {
        emit([doc.id, doc.feedId], doc.updated);
    }
}
'''

    for row in database.query(map_if_feed):
        f = Feed(row)
        if not f.disabled:
            feedlist += [f]
    print("database name: " + database.name)
    print([x.name for x in feedlist])

    for feed in feedlist:
        parsedfeed = feedparser.parse(feed.url)
        #feed.update_info(parsedfeed)

        for entry in parsedfeed.entries:
            itm = Item(entry, feed)
            print(itm.id + " / " + feed.name)
            itemstorage += [itm]

    for i in itemstorage:

        #Check keys before posting something new
        res_item_feed = database.query(map_if_key_is_known,
                keys=[i.id,i.feed['id']])

        #Kombination muss unique sein
        if len(res_item_feed) != 0:
            #Ueberpruefen ob update Zeit unterschiedlich
            pass
        else:
            database.save(i.to_dict())

        #ID ist vorhanden
