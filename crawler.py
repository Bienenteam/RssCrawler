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
        emit(doc.id, doc.feedId, doc.updated);
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
        res_item_id = database.query(map_if_key_is_known, keys=[i.id])
        #ID ist vorhanden
        if len(res_item_id) is not 0:
            
            for res_in_row in res_item_id:
                try:
                    #Hier habe ich eine feed id
                    #Keine gleiche Feed ID
                    if res_in_row.doc.feedId is not i.feedId:
                        database.save(i.to_dict())
                    #Gleiche Feed ID
                    else:
                        #Anderes Aenderungsdatum -> Update
                        if res_in_row.updated is not i.updated:
                            database.save(i.to_dict())
                except:
            #        print("Some error " )
                    database.save(i.to_dict())
                


        #ID fehlt
        else:
            database.save(i.to_dict())
