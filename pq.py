html = '''
<div class="page">
            <a href="/gongsir/8f6a2203c6eacc1a1nd53NS_.html?page=0" ka="page-prev" class="prev"></a>
        
        
        
        
        <a href="javascript:;" class="cur" ka="page-cur">1</a>
        <a href="/gongsir/8f6a2203c6eacc1a1nd53NS_.html?page=2" ka="page-2">2</a>
        <a href="/gongsir/8f6a2203c6eacc1a1nd53NS_.html?page=3" ka="page-3">3</a>
        
           
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
next_page = doc(".page .next")
print()
# print(type(doc))
# items = doc('#container li')
# print(type(items))
# for d in items.items():
#     print(type(d), d)
# lis = items.find('li')
# print(type(lis))
# print(lis)
# import requests
# from fake_useragent import UserAgent
#
# u = UserAgent()
#
# res = requests.get('https://www.zhipin.com/job_detail/c5c9559fc0d2c74f1XVy2tq6E1U~.html', headers={'User-Agent': u.random})
# print(res.status_code)
# print(res.text)