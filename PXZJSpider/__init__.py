from csv import DictReader
import pandas

import requests
result = {}
total = []
with open('pingxingzhijia2.csv', 'r', encoding='utf-8') as f:
    reader = DictReader(f)
    for row in reader:
        row = dict(row)
        total.append(row['公司名称'].strip())
        if '宝马X5' in row['车型']:
            company = row['公司名称'].strip()
            result[company] = result.get(company, 0) + 1

print(len(result.keys()))
ins = list(result.keys())
print(type(ins))
print(sum(result.values()))
obj=pandas.Series(ins)
l = obj.unique()

total = pandas.Series(total)
num = total.unique()

print(len(l))
print(len(num))