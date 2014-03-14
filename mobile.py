# coding=utf8
'''
Created on Mar 6, 2014

@author: Jayvee
'''

import urllib2
import re
import time
from scrapy.http.response.dammit import chardet
from bs4 import BeautifulSoup
from sina.crawlsina import crawler
import random
from urllib2 import URLError, HTTPError

"""
Login to Sina Weibo with cookie
"""




HEADER = {
'Host': 'weibo.cn',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
# 'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie':''} # fill with your weibo.cn cookie here

def crawl_SinaWeibo():
    start_time = time.time()
    print '任务开始'
    url = 'http://weibo.cn/XXXXXXXXXXXXXX' #需要爬的某人主页地址
    req = urllib2.Request(url, headers=HEADER)
    try:
        text = urllib2.urlopen(req).read()
    except Exception,e:
        print e
    text.encode('utf-8','ignore')
    soup = BeautifulSoup(text)
    html = soup.prettify('utf-8')
    title = soup.find('title')
    print title.text
    name = title.text  # 所读取微博的主人ID
    pagere = ((re.compile('name="mp".* value="\d*"')).search(html)).group(0)
    pagecount = (re.compile('\d+').search(pagere)).group(0)  # 读出微博总页数
    print "微博总页数：" + pagecount
    for i in xrange(int(pagecount)):
        nUrl = url+'?page='+str(i+1)   #组装新网页地址
        print '正在读取第'+str(i+1)+'/'+str(pagecount)+'页……'
        try:#允许3次超时重连    此处比较不够优雅，以后再弄
            crawler(nUrl,name,i+1)
        except Exception,e:
            print 'MOBILE1:',e
            print 5,'秒后重试'
            time.sleep(5)
            try:
                print '正在重试……'
                crawler(nUrl,name,i+1)
            except Exception,e:
                print 'MOBILE2:',e
                print 5,'秒后重试'
                time.sleep(5)
                try:
                    print '正在重试……'
                    crawler(nUrl, name, i+1)
                except Exception,e:
                    print 'MOBILE3:',e
                    print 5,'秒后重试'
                    time.sleep(5)
                    try:
                        print '正在重试……'
                        crawler(nUrl, name, i+1)
                    except Exception,e:
                        print 'MOBILE4:',e
                        print '读取第',i+1,'页失败！'
        j = random.uniform(1,2)
        print '等待',j,'秒'
        time.sleep(j)
    end_time = time.time()
    print '任务完成!爬下',name,pagecount,'页,总共耗时',(end_time - start_time),'秒'
 
    


    

if __name__ == '__main__':
    crawl_SinaWeibo()

