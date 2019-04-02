import random
import time
import pymongo as pymongo
import pymysql
import requests
from lxml import etree
from pyquery import PyQuery


class Ch168Crawler(object):
    def __init__(self, number):
        self.ROOT_URL = 'http://www.chehang168.com/index.php?c=index&m=allBrands'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }

    def _load_mongo_client(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client.crawler
        return db

    def _save2mongo(self, result):
        try:
            self.database_cursor.NYOJTItle.insert_many(result)
            return True
        except:
            return False

    def _request(self, url=None, method=None, req_type=None, **kwargs):
        if url is None:
            url = self.ROOT_URL
        if method is None:
            return False, 'not method'
        try:
            request_method = getattr(requests, method)
        except:
            return False, 'not method'
        if req_type is None:
            return False, 'not req_type'
        if isinstance(req_type, str) and req_type.lower().strip() == 'detail':
            res = request_method(url, **kwargs)
            callback = getattr(self, 'parser_detail_data')
            callback(res)
        else:
            res = request_method(url, **kwargs)
            callback = getattr(self, 'parser_list_data')
            callback(res)



    def parser_detail_data(self, res):
        pass

    def parser_list_data(self, res):
        pass

    def _save2mysql(self, result):
        pass

    def __call__(self, *args, **kwargs):
        result = []
        # for i in range(self.number+1):

        headers = {
            'Cookie': 'DEVICE_ID=92c9b8faca01eb1ddbb2504917760c37; _uab_collina=155248639781518625904579; soucheAnalytics_usertag=asa8OoSRWk; U=1237948_9ea15eb7ab1f4446a6a52b93c005d9b0'
        }
        self.headers.update(headers)
        params =
        print(res.text)



crawler = Ch168Crawler(1)
crawler()