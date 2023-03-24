import requests
import re
from datetime import timedelta, datetime


class CrawlerRate:
    def __init__(self, redis):
        self.redis = redis

    def run(self):
        rate_data = self.crawler()
        after_clean_rate_data = self.clean_data(rate_data)
        update_time = self.update_time_to_utc_plus8(rate_data)
        self.write_redis(after_clean_rate_data, update_time)
        return True

    def crawler(self):
        response = requests.get(url="https://tw.rter.info/capi.php")
        return response.json()

    def clean_data(self, __rate_data):
        new_rate_data = {}
        for key in __rate_data:
            if "USD" in key and len(key) > 3:  # 排除舊的，也排除單一的USD
                new_key = re.sub(r'^(USD)', '', key)
                new_rate_data[new_key] = __rate_data[key]['Exrate'] / __rate_data['USDTWD']['Exrate']
        # print(new_rate_data)
        return new_rate_data

    def update_time_to_utc_plus8(self, __rate_data):
        __update_time = datetime.strptime(__rate_data["USDTWD"]["UTC"], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        update_time_str = __update_time.strftime('%Y-%m-%d %H:%M:%S')
        return update_time_str

    def write_redis(self, __rate_data, __update_time):
        self.redis.hmset('rate_data', mapping=__rate_data)
        self.redis.set('update_time', __update_time)

    def read_redis(self):
        __rate_data = self.redis.hgetall('rate_data')
        __update_time = self.redis.get('update_time')
        return __rate_data, __update_time