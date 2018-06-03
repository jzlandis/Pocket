#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import sys
import time
from urlparse import urlparse

#Pocket's api url:
URL = "https://getpocket.com/v3/get"

#My unique consumer key and access token:
consKey = "61969-8870bc1a5b4db48faed3f556"
accToken = "00f9f285-be88-db9f-9093-a281aa"

parameters = {"consumer_key": consKey, "access_token": accToken, "since":0, "state":"all"}
sys.stderr.write("Sending post requests to %s with consumer_key: %s and access_token: %s\n" % (URL,consKey,accToken))
response = requests.post(URL, params=parameters)

sys.stderr.write("Status code: " + str(response.status_code) + "\n")

response_json = response.json()['list']

saved_dict = {}
#saved_dict = {item_id: (item_id,status,time_added,time_read,resolved_url,resolved_title,word_count)}
pull_keys = ('item_id','status','time_added','time_read','resolved_url','resolved_title','word_count')
pull_types = (int,bool,int,int,unicode,unicode,int)
for saved in response_json.items():
    item_id = int(saved[1]['item_id'])
    saved_dict[item_id] = tuple(f(x) for f,x in zip(pull_types,(saved[1][y] for y in pull_keys)))
sources = set()
count_articles = {}
count_words    = {}
translate_urls = {"bbc.co.uk":                     "bbc.com",
                  "texasmontly.com":               "texasmontly.com",
                  "opinionator.blogs.nytimes.com": "nytimes.com",
                  "blogs.scientificamerican.com":  "scientificamerican.com",
                  "reprints.longform.org":         "longform.org",
                  "magazine.atavist.com":          "atavist.com",
                  "read.atavist.com":              "atavist.com",
                  "stories.californiasunday.com":  "californiasunday.com",
                  "story.californiasunday.com":    "californiasunday.com",
                  "mobile.nytimes.com":            "nytimes.com",
                  "m.motherjones.com":             "motherjones.com",
                  "highline.huffingtonpost.com":   "huffingtonpost.com",
                  "features.propublica.org":       "propublica.org",
                  "features.texasmonthly.com":     "texasmontly.com",
                  "blog.longreads.com":            "longreads.com",
                  "america.aljazeera.com":         "aljazeera.com",
                  "apps.bostonglobe.com":          "bostonglobe.com",
                  "ngm.nationalgeographic.com":    "nationalgeographic.com",
                  "projects.oregonlive.com":       "oregonlive.com"}
wc_read_tot = 0
art_read_tot = 0
for s in saved_dict.items():
    s = s[1]
    if s[1] == 1:
        domain = str(urlparse(s[4]).netloc).replace("www.","")
        if domain in translate_urls.keys():
            domain = translate_urls[domain]
        wc = s[6]
        if domain in sources:
            count_articles[domain] += 1
            count_words[domain]    += wc
        else:
            sources.add(domain)
            count_articles[domain] = 1
            count_words[domain]    = wc
        wc_read_to += wc
        art_read_tot += 1
top10_by_art = sorted(count_articles.items(),key=lambda i: i[1])[-10:]
art_top10 = sum(x[1] for x in top10_by_art)
top10_by_wc = sorted(count_words.items(),key=lambda i: i[1])[-10:]
wc_top10 = sum(x[1] for x in top10_by_wc)

N = 11
