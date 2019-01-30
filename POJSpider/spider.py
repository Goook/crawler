import random
import time

import pymongo as pymongo
import pymysql
import requests
from lxml import etree


class POJCrawler(object):
    def __init__(self, number):
        self.ROOT_URL = 'http://poj.org/problem'
        self.xpath_string = "/html/body"
        self.number = number
        self.headers = {'User-Agent': 'Mozi'}
        self.database_cursor = self._load_mongo_client()

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

    def _request(self, url, params=None):
        res = requests.get(url, params=params, headers=self.headers)
        while res.status_code not in [200, 304]:
            time.sleep(random.random() * 3)
            res = requests.get(url, params=params, headers=self.headers)
        res.encoding = 'utf-8'
        return res.text

    def _parser(self, body):
        selector = etree.HTML(body)
        div_obj = selector.xpath(self.xpath_string)
        if len(div_obj):
            div_obj = div_obj[0]
        else:
            return '空数据'
        print(div_obj.text)
        title = div_obj.xpath('./div[2]')
        memory_limited, rank = div_obj.xpath("./ul/span[@class='layui-badge layui-bg-orange']")
        time_limited = div_obj.xpath("./div[@class='plm']/table/tbody/tr[1]/td[3]")
        content = div_obj.xpath("./div[@class='ptx'][1]")
        tip = div_obj.xpath("./html/body/table[2]/tbody/tr/td/div[@class='ptx'][4]")
        in_description = div_obj.xpath("./div[@class='ptx'][2]")
        out_description = div_obj.xpath("./div[@class='ptx'][3]")
        in_case = div_obj.xpath("./pre[@class='sio'][1]")
        out_case = div_obj.xpath("./pre[@class='sio'][2]")
        source = div_obj.xpath("./div[@class='ptx'][5]")
        result = {
            'title': title[0].text,
            'content': content[0].text,
            'memory_limited': memory_limited.text,
            'time_limited': time_limited[0].text,
            'rank': rank.text,
            'in_description': in_description[0].text,
            'out_description': out_description[0].text,
            'in_case': in_case[0].text,
            'out_case': out_case[0].text if len(out_case) else "",
            'tip': tip[0].text,
            'source':source[0].text,
        }
    def _save2mysql(self, result):
        pass

    def __call__(self, *args, **kwargs):
        result = []
        for i in range(self.number+1):
            time.sleep(0.1)
            params = {'id': i}
            body = self._request(self.ROOT_URL, params)
            result = self._parser(body)
            print(result)
            # status = self._save2mongo(result)



crawler = POJCrawler(1)
crawler()