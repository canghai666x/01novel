#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import socket
import time
timeout = 10
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
num = 0
#读每页文档
def readtext(url):
    bsobj = downweb(url)
    al = re.compile(r'if.*}')
    text = bsobj.find("div", {"class": "box_box"}).get_text()
    content = re.sub(al,'',text)
    title = bsobj.find("div",{"class": {"Con","box_con"}}).find("h2").get_text()
    title = re.sub(r'^\n|\n+(?=\n)|\n$', r'', title)
    content = re.sub(r'^\n|\n+(?=\n)|\n$', r'', content)
    name = bsobj.find("div", {"class": "info"}).find("a").attrs["title"]
    localdir = 'E:\code\\01novel\\novel\\'+name+'.txt'
    print("准备写入 "+name)
    with open(localdir,'a',encoding='utf-8') as f:
        f.write(title)
        f.write(content)
        print("正在写入 "+name)
    print(title+" 写入完成")
#读目录地址
def readcontents(url):
    sites = []
    html= urlopen(url).read()
    html=html.decode("gbk").encode("utf-8")
    bsobj = BeautifulSoup(html,"html.parser")
    list = bsobj.find("div",{"class": "list_box"}).findAll("a")
    for i in list:
        href = i.attrs["href"]
        sites.append(url+href)
    return sites
#读取本页小说地址列表
def gettheallnovel(url):
    novels = []
    html = urlopen(url).read()
    html = html.decode("gbk").encode("utf-8")
    bsobj = BeautifulSoup(html, "html.parser")
    divs = bsobj.findAll("div", {"class": "t"})
    for i in divs:
        novels.append(i.find("a").attrs["href"])
    return novels
#获取所有小说页地址
def alllist():
    lists = []
    for i in range(1,113):
        strs = "https://www.diyibanzhu.in/qitaleibie/shuku_0_"+str(i)+".html"
        lists.append(strs)
    return lists
def downweb(url,sleep_time=10):
    while True:
        try:
            time.sleep(sleep_time)
            html = urlopen(url).read()
            html = html.decode("gbk").encode("utf-8")
            bsobj = BeautifulSoup(html, "html.parser")
            return bsobj
        except:
            sleep_time+=5
            print("sleep_time={}".format(sleep_time))
#开始读取
lists = alllist()
for list in lists:
    novels = gettheallnovel(list)
    for novel in novels:
        contents = readcontents(novel)
        print("下载第{}本".format(num))
        for content in contents:
            readtext(content)
        print("第{}本下载完成".format(num))
        num+=1