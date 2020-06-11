#！/usr/bin/python
# —*— coding:utf-8 _*_

"""
爬取中国最好大学(www.zuihaodaxue.cn)上面的中国大学软科排行
by_0verflow qq1635590569 2020-05-22
如有写的不好的地方望不吝赐教
"""

import requests
import sys
import bs4
from prettytable import PrettyTable
from bs4 import BeautifulSoup

class ShcoolTop():
    def __init__(self, url):
        self.url = url

    def getHtmlText(self):   # 获取网页源数据
        try:
            html = requests.get(self.url)
            html.raise_for_status()   # 只取状态码为 200 的response
            html.encoding = html.apparent_encoding
            return html.text
        except:
            return ""

    def html_analyze(self, html_text, lst):   # 对上面获取到的网页源数据进行处理，并放到一个列表中
        soup = BeautifulSoup(html_text, "html.parser")   # 把response对象转为 BeautifulSoup
        for tr in soup.find("tbody").children:          # 获取表单下的所有行
            if isinstance(tr, bs4.element.Tag):        # 排除 navigablestring对象
                t = tr("td")
                lst.append([str(t[0].string), str(t[1].string), str(t[2].string), str(t[3].string), str(t[4].string)])   # 不用str()处理 NavigableString 对象的话会报错
        return lst

def print_result(lsts, num):   # 进行格式化输出
    tb = PrettyTable()
    tb.field_names = ["排名", "名字", "省份", "类型", "得分"]
    try :
        for i in range(num):
            t = lsts[i]
            tb.add_row(t)
            if i != num - 1:
                tb.add_row(["------", "----------------------", "--------", "------", "-------"])  # 增加行间隔
        print("\n[+]查询结果如下：")
        print(tb)
    except:
        print("[-]出错了，请检查操作")


def main():
    url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2020.html"   # 名单所在url
    top_num = int(sys.argv[1]) # 提取的排名前几
    lst = []
    s = ShcoolTop(url)
    html_text = s.getHtmlText()   # 获取网页原数据
    lsts = s.html_analyze(html_text, lst)   # 关键数据封装在列表中
    print_result(lsts, top_num)   # 输出

if __name__ == "__main__":
    try:
        main()
    except:
        print("""
        [使用方法]
        python China_university_rankings.py [前几数量]    # 数量最好别太大，500以内
        """)
