from ... import celery, redis
from .crawler_exchange_rate import CrawlerRate


@celery.task(name="crawler_exchange_rate")
def crawler_exchange_rate():
    crawler_rate = CrawlerRate(redis)
    crawler_rate.run()
    rate_data, update_time = crawler_rate.read_redis()
    print(rate_data, update_time)