import requests
import os 
import time
import datetime
import urllib.request as ur
from urllib.error import URLError,ContentTooShortError,HTTPError
import re
from urllib.parse import urljoin
from urllib import robotparser



def read_engine(file_name):
    engine_information = []  
    file = open(file_name,'r') 
    search_engine = file.readlines()
    for row in search_engine:  
        tmp_list = row.split(' ')
        # tmp_list[-1] = tmp_list[-1].replace('\n',',')
        engine_information.append(tmp_list)
    return engine_information



def url_check(robot_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    # 分析 哪些东西能够访问
    print('PT UA的结果: ',rp.can_fetch('*','/'))
    print('谷歌机器人的结果: ',rp.can_fetch('Googlebot','/baidu'))
    print('PT UA的结果: ',rp.can_fetch('*','http://news.baidu.com/'))
    print('谷歌机器人的结果: ',rp.can_fetch('Googlebot','/home'))
    print(rp.mtime())
    rp.modified()
    print(rp.mtime())
    # 速率
    print(rp.request_rate('*'))
    print('soso的速度: ',rp.request_rate('Sosospider').requests)
    print('ChinasoSpider的速度: ',rp.request_rate('ChinasoSpider').requests)
    print('Googlebot的速度: ',rp.request_rate('Googlebot').requests)


# def url_save():


if __name__ == '__main__':
    file_name = 'searchengine.txt'
    read_engine(file_name)
    engine_information = read_engine(file_name)
    website_url = ("http://" + "www." + str(engine_information) + ".com")
    robot_url = '{}/robots.txt'.format(website_url)
    url_check(robot_url)
