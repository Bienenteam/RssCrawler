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
