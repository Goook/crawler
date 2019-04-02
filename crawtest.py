import requests
from fake_useragent import UserAgent
from lxml import etree



user_agent = UserAgent()


headers = {
    'Cookie': 'DEVICE_ID=92c9b8faca01eb1ddbb2504917760c37; _uab_collina=155248639781518625904579; soucheAnalytics_usertag=asa8OoSRWk; U=1237463_cb04d80f535eb4446f740180ccd2e648',
    "User-Agent": user_agent.random
}
url = "http://www.chehang168.com/"

res = requests.get(url, headers=headers)

