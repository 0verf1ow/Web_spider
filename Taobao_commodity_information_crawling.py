#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
简单的淘宝商品信息爬取脚本
by_0verflow qq1635590569 2020-05-24
如有写的不好的地方望不吝赐教
"""

import math
import sys
import re
import requests
from prettytable import PrettyTable

def getHtmlText(url,user_agent,cookie):    # 获取网页响应源码
    try:
        r = requests.get(url, headers = {'user-agent' : user_agent, 'cookie' : cookie})     # 请求头更换自定义内容
        r.raise_for_status()   # 如果响应码不是200就触发异常
        r.encoding = r.apparent_encoding
        return r.text    # 返回网页源码
    except:
        return None

def htmlAnalyze(html_text):
    ls = []   # 装下所有数据
    raw_title = re.findall(r'\"raw_title\"\:\".*?\"', html_text)          # 标题
    view_price = re.findall(r'\"view_price\"\:\".*?\"', html_text)         # 价格
    item_loc = re.findall(r'\"item_loc\"\:\".*?\"', html_text)            # 所在地
    view_sales = re.findall(r'\"view_sales\"\:\".*?\"', html_text)        # 已付款人数
    nick = re.findall(r'\"nick\"\:\".*?\"', html_text)                    # 店名

    for i in range(len(raw_title)):    # 处理数据装入列表中
        title = raw_title[i].replace("\"", "").split(":")[1]     # replace("\"", "")作用是去除双引号，split(":")把信息分割成两部分，第二部分是我们要的信息
        price = view_price[i].replace("\"", "").split(":")[1]
        loc = item_loc[i].replace("\"", "").split(":")[1]
        sales = view_sales[i].replace("\"", "").split(":")[1]
        nick_name = nick[i].replace("\"", "").split(":")[1]
        ls.append((title, price, loc, sales, nick_name))    # 把数据添加进大列表中，每一个商品的信息是一个小元组
    return ls    # 返回处理完成的数据

def print_out(ls, top):    # 打印输出
    tb = PrettyTable()     # 实例化表格美化的类
    tb.field_names = ["序号", "名称", "价格", "所在地", "已付款人数", "店名"]   # 表头列名
    for i in range(top):   # 设定截取的数量
        tb.add_row([i+1, ls[i][0], ls[i][1], ls[i][2], ls[i][3], ls[i][4]])   # 添加进表的行中
        if i != (top - 1):    # 用于判断是否是最后一条信息，如果是的话就不加下面的行间隔符
            tb.add_row(["------", "------------------------------------------------------------------------------------------------------------", "--------", "-----------" ,"--------------" ,"--------------------------"])   # 行间隔符
    print(tb)   # 输出表

def main():
    """由于淘宝有反爬机制，所以我添加了自定义的 user-agent 和 cookie, 由于cookie通常有时效性如果不能用了请到浏览器找到并更换下"""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    cookie = 'v=0; cookie2=300788f39c425eb7e50bae4903a4a195; _tb_token_=eb8eee51e53bf; cna=LB1LFU0kikwCAbSIosWo+uMq; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=1434093501872503981; dnk=%5Cu6211%5Cu59D3%5Cu7CA5; tracknick=%5Cu6211%5Cu59D3%5Cu7CA5; tg=0; whl=0%260%261570459595391%261570459187862; csg=a0b20a70; skt=94530c91933f51a2; existShop=MTU3Mzc5MDMyMQ%3D%3D; _cc_=VT5L2FSpdA%3D%3D; uc1=lng=zh_CN&tag=8&cookie14=UoTbnr%2FXYScm8w%3D%3D&existShop=false&pas=0&cookie21=WqG3DMC9FxUx&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D; t=d6c0879cf658f0ce1e276dc7ff320b2f; _samesite_flag_=true; enc=cS2zgHgkVXQfeyFkA%2BvQtbLd3kg0t78qYj5jfirs66UCKvs4wWOj7FaSPvBCuGoBk3CnAy4%2FxaeI0ZOPpmSG0w%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; tfstk=c-Q5Br6aoYD5Z_bru9N2YJhEIjYdZ6h6Ou9lNi49Dzus2e55i0gwCQQPxv3vXI1..; JSESSIONID=C54C682D70173F92E0609B74D953C856; l=eBN3bK4IquKo_q0tBOfwnurza77tsIRAguPzaNbMiOCP_8fp5BZ1WZAwd9L9CnGVh6xWR35mgkfMBeYBqIv4n5U62j-lasDmn; isg=BObmTCmUhLs7alOPj1lf_LzvN1xoxyqBAooSjdCP1InkU4ZtOFQGkQchr09feyKZ'
    search = sys.argv[1]  # 搜索的关键词
    top = int(sys.argv[2])  # 需要爬取的数量
    page = math.ceil(top/44)  # 判断需要爬多少页
    for i in range(page):
        url = "https://s.taobao.com/search?q=" + search + "&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200524&ie=utf8&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s=" + str(i * 44)    # 爬取使用的url
        html_text = getHtmlText(url, user_agent, cookie)   # 给爷爬！
        if html_text != None:
            ls = htmlAnalyze(html_text)    # 接收返回的数据列表
        else:
            ls = []
            print("[-]网页爬取时出错了")
    if ls:
        print_out(ls, top)    # 打印信息
    else:
        print("[-]没有获取到数据，因该是cookie失效了，请检查")
if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("""
        [使用方法]
        python3 Taobao_commodity_information_crawling.py [搜索的关键字] [爬取的数量]
        
        如: python3 Taobao_commodity_information_crawling.py 手机 10
        """)