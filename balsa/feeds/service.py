import feedparser
import time
import asyncio
from time import mktime
from datetime import datetime
import multiprocessing
from itertools import chain
from pprint import pprint
from feeds.models import NewsFeed
from feeds.config import read_feed_config


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

def read_all_news_feeds(categories):
    feed_urls = read_feed_config()
    for url in feed_urls:
        for feed in read_news_feeds(url, categories):
            yield feed


def read_all_news_feeds_async(categories):
    async def read_news_feed_async(url, categories): 
        return list(read_news_feeds(url, categories))

    feed_urls = read_feed_config()
    event_loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(read_news_feed_async(url, categories)) for url in feed_urls]
    completed_tasks, _ = event_loop.run_until_complete(asyncio.wait(tasks))
    event_loop.close()
    return list(chain(*[completed_task.result() for completed_task in completed_tasks]))

   
if __name__=='__main__':
    categories = ['cryptocurrency', 'machine learning', 'docker']
    start = time.time()
    all_news = list(read_all_news_feeds(categories))
    end = time.time()
    print('Running time synchronously: {}'.format(end-start))
    for news in all_news:
        pprint(news.title)

    start = time.time()
    all_news = read_all_news_feeds_async(categories)
    end = time.time()
    print('Running time asynchronously: {}'.format(end-start))
    for news in all_news:
        pprint(news.title)
