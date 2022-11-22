import requests
import os 
import time
import datetime
import urllib.request as ur
from urllib.error import URLError,ContentTooShortError,HTTPError
import re
from urllib.parse import urljoin
from urllib import robotparser

# def url_check(gentleman_file):
#     urllib3.

def download(url, num_retries=2, user_agent='wswp',charset='utf-8'):
    print('Downloading:',url)
    request=ur.Request(url)
    #添加请求头(一般添加'Cookies','User-Agent')
    #默认请求头wswp (Web Scrapying With Python)
    request.add_header('User-Agent',user_agent)
    #运用异常,try...except...处理遇到一些无法控制的错误的情况:
    try:
        resp=ur.urlopen(request)
        #headers.get_content_charset()得到请求Http响应返回的字符集
        cs=resp.headers.get_content_charset()
        #如果不存在，则采用默认的字符集utf-8
        if not cs:
            cs=charset
        #decode()表示根据某种编码表示
        html=resp.read().decode(cs)
    except (URLError,ContentTooShortError,HTTPError) as e:
        #e.reason 输出错误的原因
        print('Download error:',e.reason)
        html=None
        if num_retries>0:
            #hasattr(object,name)判断对象(objedt)是否包含对应属性(name)
            if hasattr(e,'code') and (500<=e.code<600):
                #一般地说,4XX错误都是发生在请求中的,5XX错误都是发生在服务器端的
                #重下载,排除由5XX引起的错误,设定重下载次数为num_retries
                return download(url,num_retries-1)
    return html


#解析robots.txt文件，以避免下载禁止爬取的URL
def get_robots_parser(robot_url):
    rp=robotparser.RobotFileParser()
    #set_url加载robots.txt文件
    rp.set_url(robot_url)
    rp.read()
    return rp


def link_crawlinks(start_url,link_regex,robots_url=None,user_agent='wswp'):
    crawl_queue=[start_url]
    #从根目录开始爬取，只要在其url末尾加入robots.txt.
    if not robots_url:
        robots_url='{}/robots.txt'.format(start_url)
    rp=get_robots_parser(robots_url)
    #集合化crawl_queue，用于判断是否有重复元素
    seen=set(crawl_queue)
    while crawl_queue:
        #删除末尾的信息，并存储到url内
        url=crawl_queue.pop()
        #增加解析器，判断是否符合robts.txt
        if rp.can_fetch(user_agent,url):
            html=download(url,user_agent=user_agent)
            if not html:
                continue
            for link in get_links(html):
            #出现符合linke_regrex形式的url,将他保存至crawl_queue
                if re.match(link_regex,link):
                    #urljoin(url1,url2)拼接两个地址
                    abs_link=urljoin(start_url,link)
                    if abs_link not in seen:
                        #避免重复访问同一个网站
                        seen.add(abs_link)
                        crawl_queue.append(abs_link)
        else:
            print('Blocked by robots.txt:',url)

def get_links(html):
    #re.compile指定匹配的规; re.IGNORECASE忽略大小写; re.findall找到所有满足条件的信息
    webpage_regex=re.compile("""<a[^>]+href=["'](.*?)['"]""",re.IGNORECASE)
    return webpage_regex.findall(html)




if __name__ == '__main__':
    # url_base = str(input('Plz enter the website you want to visit: '))
    # url_result = ("http://" + "www." + url_base + ".com")
    # gentleman_file = (url_result + "/robots.txt")
    url = 'http://www.baidu.com'
    start_url = 'http://www.baidu.com'
    robot_url = 'http://www.baidu.com/robots.txt'
    download(url, num_retries=2, user_agent='wswp',charset='utf-8')
    get_robots_parser(robot_url)
    #link_crawlinks(start_url,link_regex,robots_url=None,user_agent='wswp')
    #get_links(html)