#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-14 17:13:31
# Project: bosszhipin

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for page in range(1,12):
            self.crawl('https://www.zhipin.com/gongsir/ce6c59163b0e3b2003F73dq_.html', params={'page': page},
                       callback=self.index_page, headers=self.headers, validate_cert=False, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #for each in response.doc('.job-list > ul > li > a').items():
          #  self.crawl(each.attr.href, callback=self.detail_page, headers=self.headers, validate_cert=False)
            self.crawl(' https://www.zhipin.com/job_detail/af93b89e723bcc521XR82N26FVA~.html', callback=self.detail_page, headers=self.headers, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        # print(type(response.doc("div[class='job-detail'] > div[class='detail-content'] >  div[class='job-sec']")))
        job_and_salary = response.doc("div[class='company-info'] div[class='name']")
        welfare_items = response.doc("div[class='info-primary'] div[class='tag-container'] div[class='job-tags'] > span").items()
        welfare = [item.text() for item in welfare_items]
        job_detail = response.doc("div[class='job-detail']")
        text_py = next(job_detail("div[class='detail-content']  div[class='job-sec']").items())
        texts = text_py("div[class='text']").text().split('\n')
        extra_info = {}
        key = "other"
        for single in texts:
            extra_info.setdefault(key, [])
            single = single.strip()
            print(single, type(single))
            print(bool(single))
            if single and (u":" == single[-1] or u"：" == single[-1]):
                key = single[:-1]
                continue
            extra_info[key].append(single)
        data = {
            "job": job_and_salary("h1").text(),
            "salary": job_and_salary("span[class='badge']").text(),
            "welfare": welfare,
            "location": response.doc("div[class='job-primary detail-box'] > div[class='info-primary'] > p").text(),
            "employer": job_detail("div[class='detail-op'] > h2[class='name']").text(),
            "employer_job": job_detail("div[class='detail-op'] > p[class='gray']").text(),
        }
        if len(extra_info['other']) == 0:
            del extra_info['other']
        data.update(extra_info)
        return data


