#!/usr/bin/python
# _*_coding:utf-8 _*_

"""未完善"""

import re
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return None

def get_StockUrl_list(html):
    stockurl_list = re.findall(r'http\://quote\.eastmoney\.com/[s][zh]\d{6}\.html', html)
    return stockurl_list

def get_StockInfo(s_list):
    ls = []
    for url in s_list:
        html = get_html_text(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            if soup("h2", {"class": "header-title-h2 fl"}):
                soup = BeautifulSoup(html, 'html.parser')
                name = str(soup("h2", {"class": "header-title-h2 fl"})[0].string)    # 股票名称
                code = str(soup("b", {"class":"header-title-c fl"})[0].string)       # 股票代码
                today_open = str(soup(id='gt1')[0].string)      # 今开
                the_highest = str(soup(id='gt2')[0].string)     # 最高
                limit_up = str(soup(id='gt3')[0].string)        # 涨停
                turnover_rate = str(soup(id='gt4')[0].string)   # 换手
                turnover = str(soup(id='gt5')[0].string)         # 成交量
                pe_ratio = str(soup(id='gt6')[0].string)        # 市盈
                total_value = str(soup(id='gt7')[0].string)     # 总市值
                ls.append({'name':name, 'code':code, 'today_open':today_open, 'the_highest':the_highest, 'limit_up':limit_up, 'turnover_rate':turnover_rate, 'turnover':turnover, 'pe_ratio':pe_ratio, 'total_value':total_value})
    return ls

def print_out(ls):
    tb = PrettyTable()
    tb.field_names = ["股票名称", "股票代码", "今开", "最高", "涨停", "换手", "成交量", "市盈", "总市值"]
    for i in range(len(ls)):
        tb.add_row([ls[i]['name'], ls[i]['code'], ls[i]['today_open'], ls[i]['the_highest'], ls[i]['limit_up'], ls[i]['turnover_rate'], ls[i]['turnover'], ls[i]['pe_ratio'], ls[i]['total_value']])
    print(tb)




html = get_html_text("http://quote.eastmoney.com/stock_list.html")
s_list = get_StockUrl_list(html)
ls = get_StockInfo(s_list)
print_out(ls)