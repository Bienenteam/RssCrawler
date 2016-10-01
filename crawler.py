#Web Crawler for receiving RSS/Atom feeds
import feedparser
import couchdb
from couchdb import Server
import os
from feed import Feed
from item import Item


if __name__ == "__main__":
    server = Server(os.environ['COUCHURL'])
    database = server['simdata']
    map_feeds = '''
function(doc) {
    if( doc.type == "feed" ){
        emit( doc._id , doc.url);
    }
}
'''

    for row in database.query(map_feeds):
        print("Feed: " + row.value)
        parsedfeed = feedparser.parse(row.value)
        for entry in parsedfeed.entries:
            itm = Item(entry)
            itm.setFeedId( row.id )
            map_duplicates = 'function(doc) {if (doc.type == "item" && doc.feedId == "' + row.id + '" && doc.id == "' + itm.id + '") emit(doc.id, doc.updated);}'
            dup_query = database.query(map_duplicates)
            for entry in dup_query: # Check for duplicates
                if entry.value != itm.updated: # ...and wether they are outdated.
                    #TODO update this entry
                    print('Update this!')
            if len(dup_query) == 0: # save a new entry if there are no duplicates
                database.save(itm.to_dict())
                print('  New Entry found: ' + itm.title)
