import re,requests
from bs4 import BeautifulSoup


# ptt = soup.find_all(name='div', attrs={"class":"ptt"})[0]
#获取小标题
def get_title(soup):
    return soup.find_all(name='p', attrs={"class":"pst"})
#获取文本
def get_text(soup):
    return soup.find_all(name='div', attrs={"class":"ptx"})
#获取样例
def get_sample(soup):
    return soup.find_all(name='pre', attrs={"class":"sio"})

print("Please input URL:")
url = input()
html = requests.get(url)
soup = BeautifulSoup(html.text, "lxml")


text_list = get_text(soup)[0:3]
title_list = get_title(soup)[0:5]
sample_list = get_sample(soup)

text = list()
title = list()
all = list()
#处理文本 加换行符
for i in text_list:
    text.append(i.text + '\r\n')
for i in title_list:
    title.append("#### " + i.text + '\r\n')
for i in sample_list:
    i = '```\r\n' + i.string + '\r\n' + '```\r\n'
    text.append(i)


for i in range(5):
    all.append(title[i] + text[i])
URL = '[题目链接]' + '(' + url + ')' + '\r\n'
f = open('POJ.txt', 'w')
f.write(URL)
for i in all:
    f.write(i)
f.write("#### AC\n- ")
f.close()
print("Done!")
