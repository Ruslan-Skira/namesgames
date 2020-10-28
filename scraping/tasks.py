# tasks
from __future__ import absolute_import, unicode_literals

from datetime import datetime

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.exceptions import Reject
# logger
from celery.utils.log import get_task_logger

# job model
from .models import People



logger = get_task_logger(__name__)


@shared_task(serializer='json')
def scraping_response(name='https://news.ycombinator.com/rss'):
    article_list = []
    try:
        r = requests.get(name)
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.find_all('item')
        for article in articles:
            title = article.find('title').text
            link = article.find('link').text
            published_wrong = article.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')

            article_full = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HakerNews RSS'
            }
            article_list.append(article_full)
            return save_function(article_list)

    except Exception as e:
        print('The scraping job failes exception is')
        print(e)


@shared_task(serializer='json')
def save_function(article_list):
    # timestamp and filename
    source = article_list[0]['source']
    new_count = 0
    print(source)

    error = True

    try:
        latest_article = People.objects.filter(source=source).order_by('-id')[0]
    except Exception as e:
        print(f'Exception \n {e}')
        error = False
        pass
    finally:
        if error is not True:
            latest_article = None
        for article in article_list:
            if latest_article is None:
                try:
                    People.objects.create(
                        title=article['title'],
                        link=article['link'],
                        published=article['published'],
                        source=article['source']
                    )
                    new_count += 1
                except Exception as e:
                    print(f'{e} \n Exception')
                    break
            elif latest_article.published == None:
                try:
                    People.objects.create(
                        title=article['title'],
                        link=article['link'],
                        published=article['published'],
                        source=article['source']
                    )
                    new_count += 1
                except:
                    print('failed at latest_article.published == none')
                    break
            elif latest_article.source == None:
                try:
                    People.objects.create(
                        title=article['title'],
                        link=article['link'],
                        published=article['published'],
                        source=article['source']
                    )
                    new_count += 1
                except:
                    print('failed at latest_article.source == none')
                    break
            elif latest_article.published < article['published']:
                try:
                    People.objects.create(
                        title=article['title'],
                        link=article['link'],
                        published=article['published'],
                        source=article['source']
                    )
                    new_count += 1
                except:
                    print('failed at latest_article.published < j[published]')
                    break
            else:
                return 'news scraping failed, date was more recent than last published date'

        logger.info(f'New articles: {new_count} articles(s) added.')
        return 'finished'


@shared_task
def div(x, y):
    try:
        z = x / y
        return z
    except ZeroDivisionError as exc:
        raise Reject(exc, requeue=False)
