import random
import time

import pymongo as pymongo
import pymysql
import requests
from lxml import etree


class Crawler(object):
    def __init__(self, number):
        self.ROOT_URL = 'http://nyoj.top/problem/'
        self.xpath_string = "/html/body/div[@class='layui-container']/div[@class='layui-row layui-col-space15']/div[@class='layui-col-md8']/div[@class='problem-content']"
        self.number = number
        self.headers = {'User-Agent': 'Mozi'}
        self.database_cursor = self._load_mongo_client()

    def _load_mongo_client(self):
        pass

    def _save2mongo(self, result):
        pass

    def _request(self, url, method=None, **kwargs):
        res = requests.get(url, params=params, headers=self.headers)
        while res.status_code not in [200, 304]:
            time.sleep(random.random() * 3)
            res = requests.get(url, params=params, headers=self.headers)
        res.encoding = 'utf-8'
        return res.text

    def _parser(self, body):
        pass
    def _save2mysql(self, result):
        pass

    def __call__(self, *args, **kwargs):
        pass

