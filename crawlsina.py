# coding=utf-8
'''
Created on Mar 7, 2014

@author: Jayvee
'''
import urllib2
from bs4 import BeautifulSoup
import re
from urllib2 import URLError, HTTPError
import socket



HEADER = {
'Host': 'weibo.cn',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
# 'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie':''}#填入你的Weibo.cn的Cookie

class MyException(Exception):
    pass

def crawler(url, name, page):
    socket.setdefaulttimeout(10)
    req = urllib2.Request(url, headers=HEADER)
    try:
        html = urllib2.urlopen(req).read()
    except urllib2.URLError, e:
        if isinstance(e.reason, socket.timeout):  
            raise MyException("There was an error: %r" % e)  
        else:  
        # reraise the original error  
            raise
    finally:
#         req.close()
        pass
    soup = BeautifulSoup(html)
    result = soup.findAll('div', {'class':'c'})  # 搜索所有的单个微博信息
    for i in xrange(len(result) - 2):  # 遍历本页所有微博,除了最后两个（它们是页面底框）
        text = '';  # 待写入的字符串
        text = text + str((page - 1) * 50 + i) + ':\n'#加入序号
        test = result[i]
        isPost = len(test.findAll('span', 'cmt'))  # 若有cmt标签存在，则为转发微博，否则为原创微博
        if isPost == 0:  # 0则为原创微博，只有ctt标签
            temp = test.findAll('span')[0].text + '\t' + test.findAll('span')[1].text
            text = text + str(temp) + '\n'
        else:
            if(isPost == 2):#好友圈可见的微博
                temp = (str(test.find('span','cmt').text)+str(test.find('span','ctt').text).replace('\n', '')+'\t'+str(test.find('span','ct').text)).replace(' ', '')
            elif (isPost == 1):#置顶微博或已赞微博
                if (len(test.findAll('span','kt'))==0):#即不是顶置微博，是已赞的原创微博
                    temp = test.findAll('span')[0].text + '\t' + test.findAll('span')[1].text
                    text = text + str(temp) + '\n'
                else:
                    try:
                        temp = (str(test.find('span','kt').text)+str(test.find('span','cmt').text)+str(test.find('span','ctt').text).replace('\n', '')+'\t'+str(test.find('span','ct').text)).replace(' ', '')
                    except Exception,e:
                        print '错误位置：',i
                        print isPost
                        exit()
            else:#普通转发微博
                temp = (str(test.findAll('span', limit=2)[0].text) + str(test.findAll('span', limit=2)[1].text)).replace('\n', '').replace(' ', '')
                text = text + str(temp) + '\n'
                # 需要判断是否有转发图片
                if len(test.findAll('div')) < 3:  # 无图片
                    tt = test.findAll('div')[1].text.replace('\n', '').replace(' ', '')
                else:  # 有图片
                    tt = test.findAll('div')[2].text.replace('\n', '').replace(' ', '')
                temp =  re.compile(u'赞\[\d*\].*收藏').sub('\t', tt)
            text = text  +str(temp) + '\n'
        #输出对应的发送时间文本    
        tp = open(name + '发送时间.txt', 'a+')
        time = test.find('span','ct').text.replace('\n', '').replace(' ', '')
        tp.write(str((page - 1) * 50 + i)+':\t'+time+'\n')
        tp.close()
        #输出微博文本
        fp = open(name + '.txt', 'a+')
        fp.write(text)
        fp.close()
    print '第'+str(page)+ '页读取完毕'
