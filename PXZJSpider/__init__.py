import json
import time
import csv
from fake_useragent import UserAgent
import requests

user_agent = UserAgent()

# headers = {
#     'User-Agent': user_agent.random
# }


# res = requests.get('https://parallel-home-web.maiche.com/api/web/brand-web/get-grouped-brand-list.htm?_=0.40605995379378435', headers=headers)
#
# data = json.loads(res.content)
#
#
# item_list = data['data']['itemList']
#
#
#
# brandid_list = []
#
#
# # for item in item_list:
# #     for ids in item['brandList']:
# #         brandid_list.append(ids['id'])
# #
# # url = 'https://parallel-home-web.maiche.com/api/web/v2/product/get-product-list-by-condition.htm'
start = time.time()
url = 'https://parallel-home-web.maiche.com/api/web/v2/product/get-product-list-by-condition.htm'
result = []
try:
    with open('pingxingzhijia.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['电话', '颜色', '价格', '类型', '公司名称', '配置', '车型', '公司地址', '车源所在地']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 190):
            time.sleep(1)
            headers = {
                'User-Agent': user_agent.random
            }
            params = {
                'pageSize': 100,
                'page': index,
                '_': 0.860832177359355,
            }
            print('正在爬取第%d页' % index)
            res = requests.get(url, params=params, headers=headers)
            data = json.loads(res.content)
            detail_data = data.get('data', [])
            print('状态%s,数据量%s' % (res.status_code, len(detail_data)))
            for single in detail_data:
                single_data = {
                    '公司名称': single.get('dealerName', ""),
                    '配置': single.get('configInfos', []),
                    '电话': single.get('contactList', []),
                    '车型': single.get('productName', []),
                    '价格': single.get('price', ""),
                    '颜色': single.get('color', ""),
                    '类型': single.get('productType', ""),
                    '车源所在地': single.get('locatedCity', ""),
                    '公司地址': single.get('dealerAddress', ""),
                }
                result.append(single_data)
                writer.writerow(single_data)
except Exception as e:
    print(e)
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['电话', '颜色', '价格', '类型', '公司名称', '配置', '车型', '公司地址', '车源所在地']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(result)

print(time.time() - start)

