#Web Crawler for receiving RSS/Atom feeds
import feedparser

feedurls = []
feedurls += [r'./test/example.xml']

itemstorage = []

class Feed(object):
    items = []
    def __init__(self, parsedfeed):
        self.title = parsedfeed['feed']['title']
        self.link = parsedfeed['feed']['link']
        self.subtitile = parsedfeed['feed']['subtitle']

class Item(object):
    def __init__(self, item_dict, feed):
        try:
            self.title = item_dict['title']
        except:
            self.title = ""
        try:
            self.id = item_dict['id']
        except:
            self.id = ""
        try:
            self.link = item_dict['link']
        except:
            self.link = ""
        try:
            self.published = item_dict['published']
        except:
            self.published = ""
        try:
            self.updated = item_dict['updated']
        except:
            self.updated = ""
        try:
            self.summary = item_dict['summary']
        except:
            self.summary = ""
        try:
            self.content = item_dict['content']
        except:
            self.content = ""
        self.feed = feed

if __name__ == "__main__":
    for url in feedurls:
        parsedfeed = feedparser.parse(url)
        print(parsedfeed.feed.title)
        feed = Feed(parsedfeed)
        for entry in parsedfeed.entries:
            itm = Item(entry, feed)
            itemstorage += [itm]

    for i in itemstorage:
        print(i.title + "  | FROM | " + i.feed.title)
        print("====================================")

