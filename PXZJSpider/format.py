import csv



# 公司名称  配置	电话__callPhone	电话__name	电话__showPhone	车型	价格	颜色	类型	车源所在地	公司地址
import json

result = []
with open('pingxingzhijia2.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = dict(row)
        row['配置'] = eval(row['配置'])
        row['\ufeff电话'] = eval(row['\ufeff电话'])
        max_length = max(map(lambda x: len(x) if isinstance(x,list) else 1, row.values()))
        mid = [[""] * 11 for i in range(max_length)]
        for i in range(max_length):
            mid[i][1] = row['配置'][i] if i < len(row['配置']) else ""
            mid[i][2] = row['\ufeff电话'][i].get('callPhone',"") if i < len(row['\ufeff电话']) else ""
            mid[i][3] = row['\ufeff电话'][i].get('name', "") if i < len(row['\ufeff电话']) else ""
            mid[i][4] = row['\ufeff电话'][i].get('showPhone', "") if i < len(row['\ufeff电话']) else ""
        mid[0][0] = row['公司名称']
        mid[0][5] = row['车型']
        mid[0][6] = row['价格']
        mid[0][7] = row['颜色']
        mid[0][8] = row['类型']
        mid[0][9] = row['车源所在地']
        mid[0][10] = row['公司地址']
        result += mid

with open('test_format.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    fieldnames = ['公司名称','配置', '电话__callPhone', '电话__name', '电话__showPhone', '车型', '价格', '颜色', '类型', '车源所在地', '公司地址']
    writer.writerow(fieldnames)
    for l in result:
        writer.writerow(l)

