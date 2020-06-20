#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

import requests
from lxml import etree

"""获取商品数量"""
def get_JDcard_num():
    url = "https://src.sjtu.edu.cn/gift/4/"    # 商品信息页面
    try:
        r = requests.get(url)
        html = etree.HTML(r.text)   # 转为 etree对象
        num = str(html.xpath('/html/body/div/div/div[1]/div/div/div[3]/div[2]/span/strong/text()')[0])   # xpath获取数量关键字
        return num
    except:
        print("[!]网页爬取出错，请手动检查")
        get_JDcard_num()    # 重新爬取

"""发邮件"""
def send_Email(send_mail, key, person, num, smtp_server):
    ret = True
    if re.findall(r'@\w+.com', send_mail)[0] == '@qq.com':  # 判断是否qq邮箱
        smtp_server = "smtp.qq.com"
    elif re.findall(r'@\w+.com', send_mail)[0] == '@163.com':  # 判断是否网易邮箱
        smtp_server = "smtp.163.com"
    try:
        msg = MIMEText('JD卡上架了，数量还有 ' + num + '个', 'plain', 'utf-8')  # 括号第一个参数就是邮件主体信息
        msg['From'] = formataddr(["wooyun路人甲", send_mail])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["尊敬的白帽子", 'xxxxx@163.com'])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Edu_src京东卡上架通知"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(smtp_server, 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(send_mail, key)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(send_mail, person, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
        s = "[!]错误信息：" + str(e)
        output_log(s)
    return ret

"""写日志,打印信息"""
def output_log(s):    
    print(s)
    with open('log.txt', 'a', encoding='utf-8') as log:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log.write(t + "   " + s + "\n")

def main():
    num = get_JDcard_num()   # 获取网页内的JD卡数量
    if num != '0':
        ret = send_Email(send_mail, key, person, num, smtp_server="")    # 调用发送邮件
        if ret:
            s = "[+]检测到京东卡已上架，邮件发送成功"
            output_log(s)
        else:
            s = "[!]检测到京东卡已上架，但邮件发送失败"
            output_log(s)
    else:
        s = "[-]没上架"
        output_log(s)
if __name__ == '__main__':
    #[配置区域]
    send_mail = 'xxxxxx@qq.com'  # 发件人邮箱账号
    key = 'xxxxxxxxxxxxx'  # 发件人邮箱密码(当时申请smtp给的口令)
    person = 'xxxxxxxxx@qq.com'  # 收件人邮箱账号，多个收件人的话写成列表形式
    # with open('email.txt', 'r', encoding="utf-8") as f:   # 群发邮件的话在目录下建个 email.txt,一行一个邮箱地址；不群发就注释这行跟下面那行代码
        # person = [i.strip() for i in f]

    while True:   # 一直检测
        main()
        time.sleep(300)   # 设置多久检测一次有没有上架，默认五分钟
