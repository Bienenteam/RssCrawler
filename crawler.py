#Web Crawler for receiving RSS/Atom feeds
import feedparser

feedurls = []
feedurls += [r'./test/example.xml']

itemstorage = []

class Feed(object):
    items = []
    def __init__(self, title, link, subtitle):
        self.title = title
        self.link = link
        self.subtitile = subtitle

class Item(object):
    def __init__(self, item_dict, feed):
        self.title = item_dict['title']
        #self.id = item_dict['id']
        self.link = item_dict['link']
        self.published = item_dict['published']
        self.updated = item_dict['updated']
        self.summary = item_dict['summary']
#        self.content = item_dict['content']
        self.feed = feed

if __name__ == "__main__":
    for url in feedurls:
        parsedfeed = feedparser.parse(url)
        print(parsedfeed.feed.title)
        feed = Feed(
                parsedfeed['feed']['title'],
                parsedfeed['feed']['link'],
                parsedfeed['feed']['subtitle'])
        for e in parsedfeed.entries:
            i = Item(e, feed)
            itemstorage += [i]

    for i in itemstorage:
        print(i.title + " FROM " + i.feed.title)
        print("====================================")

