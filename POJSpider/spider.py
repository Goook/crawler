import random
import re
import sys
import time

import pymongo as pymongo
import pymysql
import requests
from lxml import etree


class POJCrawler(object):
    def __init__(self, number):
        self.ROOT_URL = 'http://poj.org/problem'
        self.xpath_string = "/html/body/table[2]/tr/td"
        self.number = number
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        # self.database = self._load_mongo_client()
        self.database = self._load_mysql_client()
        self.offset = 1617

    def _load_mysql_client(self):
        self.mysql_client = pymysql.connect(host='39.96.194.42',
                                            user='root',
                                            password='bamboo',
                                            database='letcode',
                                            port=3306)
        return self.mysql_client.cursor()




    def _load_mongo_client(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client.crawler
        return db

    def _save2mongo(self, result):
        try:
            self.database.NYOJTItle.insert_many(result)
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

    def _format_rank(self, num_cm, num_ac):
        print(num_cm)
        print(re.findall(r'[0-9]+', str(num_cm)))

        # num_cm = int()
        # num_ac = int(re.findall(r'\d+', str(num_ac))[0])
        if num_cm / num_ac < 0.3:
            return 3
        elif num_cm / num_ac > 0.45:
            return 1
        else:
            return 2

    def _parser(self, body):
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(body)
        # return 'kong'
        selector = etree.HTML(body)
        div_obj = selector.xpath(self.xpath_string)
        if div_obj:
            div_obj = div_obj[0]
        else:
            return None
        title = div_obj.xpath('./div[2]')
        memory_limited = div_obj.xpath("./div[@class='plm']/table/tr[1]/td[3]")
        time_limited = div_obj.xpath("./div[@class='plm']/table/tr[1]/td[1]")
        number_accepted = div_obj.xpath("./div[@class='plm']/table/tr[2]/td[1]")[0]
        number_commited = div_obj.xpath("./div[@class='plm']/table/tr[2]/td[3]")[0]
        content = div_obj.xpath("./div[@class='ptx'][1]")
        tip = div_obj.xpath("./div[@class='ptx'][4]")
        in_description = div_obj.xpath("./div[@class='ptx'][2]")
        out_description = div_obj.xpath("./div[@class='ptx'][3]")
        in_case = div_obj.xpath("./pre[@class='sio'][1]")
        out_case = div_obj.xpath("./pre[@class='sio'][2]")
        source = div_obj.xpath("./div[@class='ptx']//a")
        result = {
            'title': title[0].text,
            'content': content[0].text,
            'memory_limited': 64,
            'time_limited': 1000,
            'rank': 1,
            'in_description': in_description[0].text,
            'out_description': out_description[0].text if out_description else "",
            'in_case': in_case[0].text if len(out_case) else "",
            'out_case': out_case[0].text if len(out_case) else "",
            'tip': tip[0].text if tip else "没有任何提示哦",
            'source':source[0].text,
            'number_accepted': 0,
            'number_commited': 0,
        }
        return result
    def _save2mysql(self, result):
        key = ','.join(result.keys())
        value = ','.join(map(lambda x: '"' + str.replace(str(x), "'", '\\\'') + '"', result.values()))
        try:
            self.database.execute("""INSERT INTO problem(%s) values(%s)""" % (key, value))
        except Exception as e:
            print(e)
            return False
        return True



    def __call__(self, *args, **kwargs):
        try:
            result = []
            begin = time.time()
            for i in range(self.offset, self.offset + self.number):
                time.sleep(0.1)
                params = {'id': i}
                body = self._request(self.ROOT_URL, params)
                result = self._parser(body)
                status = self._save2mysql(result)
                print(i, status)
            print('cost', time.time() - begin)
            self.database.close()
        except Exception as e:
            raise e
        finally:
            self.mysql_client.commit()
            self.mysql_client.close()

crawler = POJCrawler(500)
crawler()