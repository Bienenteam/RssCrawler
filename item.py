from uuid import uuid4
import hashlib

class Item(object):
    def __init__(self, item_dict):
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
        try:
            self.feedId = str(item_dict['feedId'])
        except:
            self.feedId = ""

    def setFeedId(self, feedId):
        self.feedId = feedId

    def to_dict(self):
        return {
                '_id': uuid4().hex,
                'type': 'item',
                'schemaversion': 2,
                'feedId': self.feedId,
                'title': self.title,
                'link': self.link,
                'id': self.id,
                'published': self.published,
                'updated': self.updated,
                'summary': self.summary,
                'content':  self.content
                }
