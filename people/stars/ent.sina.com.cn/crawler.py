#!/usr/bin/env python
# -*- encoding: utf-8; indent-tabs-mode: nil -*-
"""
    crawler
    ~~~~~~~

    desc

    :copyright: (c) 2015 Menglong TAN.
"""

import os
import sys
import re
import urllib2
import time
import BeautifulSoup
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(fmt)
logger.addHandler(ch)

class Star(object):
    def __init__(self):
        self.name = ""
        self.gender = ""
        self.nation = ""
        self.birth = ""
        self.horoscope = ""
        self.height = ""

    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s\t%s" % (self.name, self.gender, self.nation,
                                           self.birth, self.horoscope,
                                           self.height)

def extract_list(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
    req = urllib2.Request(url, headers=headers)
    resp = None
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "Error Code:", e.code
        return
    except urllib2.URLError, e:
        print "Error Reason:", e.reason
        return

    soup = BeautifulSoup.BeautifulSoup(resp.read())
    stars = []
    for star in soup.findAll("div", attrs={"class":"item-intro left"}):
        s = Star()
        s.name = str(star.find("a", attrs={"style":"overflow: hidden;text-overflow: ellipsis;white-space: nowrap;width:140px;"}).contents[0]).strip()
        for p in star.findAll("p"):
            if str(p.contents[0]).startswith("<span class=\"txt\">性别:</span>"):
                s.gender = str(p.contents[1]).strip()
            elif str(p.contents[0]).startswith("<span class=\"txt\">国籍:</span>"):
                s.nation = str(p.contents[2]).strip()
            elif str(p.contents[0]).startswith("<span class=\"txt\">出生日期:</span>"):
                s.birth = str(p.contents[1]).strip()
            elif str(p.contents[0]).startswith("<span class=\"txt\">星座:</span>"):
                s.horoscope = str(p.contents[1].contents[0]).strip()
            elif str(p.contents[0]).startswith("<span class=\"txt\">身高:</span>"):
                s.height = str(p.contents[1]).strip()
            
        stars.append(s)
    return stars

if __name__ == "__main__":
    list_url = "http://ku.ent.sina.com.cn/star/search&page_no="
    total_page = 1068
    f = open("stars.dat", "w+")
    for i in range(total_page):
        logger.info("progress: %d/%d", i + 1, total_page)
        stars = extract_list(list_url + str(i + 1))
        for star in stars:
            f.write(str(star) + "\n")
            f.flush()
        time.sleep(2)
    f.close()

