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
    games = []

    cnt = 0
    for html in soup.findAll("a", attrs={"class":"link"}):
        games.append(str(html.contents[0]))
        cnt += 1
        logger.info("progress: %d", cnt)

    return games

if __name__ == "__main__":
    list_url = "http://www.17173.com/zq/all.shtml"
    f = open("games.dat", "w+")
    logger.info("progress")
    games = extract_list(list_url)
    for game in games:
        f.write(game + "\n")
        f.flush()
    f.close()

