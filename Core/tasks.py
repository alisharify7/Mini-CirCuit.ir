from Core.extensions import RedisServer

from celery import shared_task

from lib.crawler.currency import get_cny_current_price


@shared_task(ignore_result=True)
def set_cny_currency_in_redis():
    """
    getting cny_currency from source and  set it in redis
    """
    result = get_cny_current_price()
    if result:
        print(
            f"current price: {result}, source : https://www.tgju.org/profile/price_cny"
        )
        RedisServer.set(name="currency_price", value=result, ex=60 * 5)
    else:
        print(f"cant fetch price")


set_cny_currency_in_redis()
