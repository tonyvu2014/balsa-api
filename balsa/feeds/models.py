class NewsFeed(object):

    def __init__(self, title, link, description, published_date):
        self.title = title
        self.link = link
        self.description = description
        self.published_date = published_date

    def __str__(self):
        return u"Title: {title}\nURL: {url}\nDescription: {desc}".format(title=self.title, url=self.link, desc=self.description).encode('utf-8') 
