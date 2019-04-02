import random
import time

import pymongo as pymongo
import pymysql
import requests
from lxml import etree


class NYOJCrawler(object):
    def __init__(self, number):
        self.ROOT_URL = 'http://nyoj.top/problem/'
        self.xpath_string = "/html/body/div[@class='layui-container']/div[@class='layui-row layui-col-space15']/div[@class='layui-col-md8']/div[@class='problem-content']"
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
            return []
        title = div_obj.xpath('./ul[1]/h1')
        # memory_limited, rank = div_obj.xpath("./ul/span[@class='layui-badge layui-bg-orange']")
        # time_limited = div_obj.xpath("./ul/span[@class='layui-badge']")
        content = div_obj.xpath("./div[@class='fly-panel'][1]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
        print(content.text)
            # tip = div_obj.xpath("./div[@class='fly-panel'][6]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
            # in_description = div_obj.xpath("./div[@class='fly-panel'][2]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
            # out_description = div_obj.xpath("./div[@class='fly-panel'][3]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
            # in_case = div_obj.xpath("./div[@class='fly-panel'][4]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
        # print(in_description)
        # out_case = div_obj.xpath("/div[@class='fly-panel'][5]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']")
        # source = div_obj.xpath("./div[@class='fly-panel'][7]/div[@class='nyoj-problem-content']/div[@class='nyoj-problem-content-col nyoj-clear-width']/a[@class='fly-link']")
        # result = {
        #     'title': title[0].text,
        #     'content': content[0].text,
        #     'memory_limited': memory_limited.text,
        #     'time_limited': time_limited[0].text,
        #     'rank': rank.text,
        #     'in_description': in_description[0].text,
        #     'out_description': out_description[0].text,
        #     'in_case': in_case[0].text,
        #     'out_case': out_case[0].text if len(out_case) else "",
        #     'tip': tip[0].text,
        #     'source':source[0].text,
        # }
        # print(result)
    def _save2mysql(self, result):
        pass

    def __call__(self, *args, **kwargs):
        result = []
        # for i in range(self.number+1):
        time.sleep(0.1)
        url = self.ROOT_URL + str(12)
        body = self._request(url)
        result = self._parser(body)
        print(result)
            # status = self._save2mongo(result)



crawler = NYOJCrawler(1)
crawler()