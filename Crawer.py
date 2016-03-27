#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import re
import Queue
import json

class JD:

    def __init__ (self, baseUrl):
        self.baseURL = baseUrl
        self.q = Queue.Queue(maxsize = 1000)
        self.q.put(self.baseURL)
        self.response = None
        self.num = 0
        self.s = set([self.baseURL])
        self.file = None

    #get the url from collection and get the page
    def get_page (self):
       self.baseURL = self.q.get()
       url = self.baseURL
       print url
       try:
           request = urllib2.Request(url)
           response = urllib2.urlopen(request)
           result = response.read().decode('gbk')
           self.s.add(self.baseURL)
           self.num = self.num + 1
           return result
       except urllib2.URLError, e:
           if hasattr(e, "reason"):
               print u"error, reason：", e.reason
               return None

    # remove some useless imformation , get the content and some urllib
    def get_name (self):
        self.response = self.get_page()
        pattern_name = re.compile('<div id="name">.*?<h1>(.*?)</h1>', re.S)
        item_name = re.search(pattern_name,self.response)

        print u"item_name is : ",item_name.group(1).strip()
        return item_name.group(1).strip()


    def get_product (self):
        pattern_pro = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(pattern_pro,self.response)[0]
        return product_info
    
    def get_product_skuid (self):
        product_info = self.get_product()
        skuid_re = re.compile(r'skuid: (.*?),', re.S)
        skuid = re.findall(skuid_re, product_info)[0]
        return skuid

    def get_product_price (self):
        skuid = self.get_product_skuid()
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'
        price_json = json.load(urllib.urlopen(url))[0]
        if price_json['p']:
            price = price_json['p']
            print u"price is : ", price
            return price

    def get_url (self):
        pattern = re.compile('<div class="p-img"><a href="//(.*?)" title.*?>.*?', re.S)
        result = re.findall(pattern, self.response)
        for res in result:
            if res not in self.s:
                print res
                if not self.q.full():
                    self.q.put("http://" + res)
                else:
                    break
    
    def write (self, name, price):
        self.file.write("\nname: ")
        self.file.write(name.encode('utf-8'))
        self.file.write("\nprice: ")
        self.file.write(price.encode('utf-8'))
        self.file.write("\n")
        self.file.write("URL: " + self.baseURL + "\n")




baseUrl = 'http://item.jd.com/1133142983.html'
jd = JD(baseUrl)
jd.get_name()
jd.get_product_price()
jd.get_url()

i = 0
jd.file = open("jd.txt", "w+")
while i < 1000:
    jd.write(jd.get_name(), jd.get_product_price())
    jd.get_url()
    i = i + 1


jd.file.close()

