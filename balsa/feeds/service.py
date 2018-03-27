import feedparser
from time import mktime
from datetime import datetime
import multiprocessing
from itertools import chain
from pprint import pprint
from feeds.models import NewsFeed
from feeds.config import read_feed_config
from feeds.common import unpack_args


def read_news_feeds(url, categories):    
    def has_category(post):
        if post.get('tags') is None:
            return False
        for tag in post.get('tags'):
            if tag['term'].lower() in categories:
                return True
        return False             
    
    feed = feedparser.parse(url)
    for post in feed.entries:
          if has_category(post):
              yield NewsFeed(post.title, post.link, post.description, datetime.fromtimestamp(mktime(post.published_parsed)))


@unpack_args    
def read_news_feed_wrapper(url, categories):
    return list(read_news_feeds(url, categories))


def read_news_feed_in_parallel(urls, categories):
    pool_size = multiprocessing.cpu_count() * 2
    process_pool = multiprocessing.Pool(processes=pool_size)
    news_list = process_pool.map(read_news_feed_wrapper, [(url, categories) for url in urls])
    return list(chain(*news_list))


def read_all_news_feeds(categories):
    feed_urls = read_feed_config()
    for url in feed_urls:
        for feed in read_news_feeds(url, categories):
            yield feed


if __name__=='__main__':
    feeds = read_all_news_feeds(['mobile', 'api', 'cryptocurrency'])
    for f in feeds:
        pprint(f)