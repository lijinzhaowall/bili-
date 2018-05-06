import requests
from bs4 import BeautifulSoup
import json
import threading
from concurrent import futures
import time
import urllib

lock = threading.Lock()
def onepage(list):
    list = str(list)
    print(list)
    url = list
    #  url = 'https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id='+list
    #  url = 'https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id=3705833'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    web_data = requests.get(url,headers=headers,timeout=6).json()
    #soup = BeautifulSoup(web_data.text, 'lxml')
    time.sleep(0.5)
    try:
        up_name = web_data['data']['user']['name']                             #up名字
        img_name = web_data['data']['item']['title']                           #图名
        upload_time = web_data['data']['item']['upload_time']                  #图上传时间
        collect = web_data['data']['item']['collect_count']                    #收藏数
        like = web_data['data']['item']['like_count']                          #喜欢数
        x = len(web_data['data']['item']['pictures'])
        for i in range(0, x):
            img_src = web_data['data']['item']['pictures'][i]['img_src']       #图链接
            if collect >= 5:                                                   #过滤条件
                with lock:
                    print('成功：{}'.format(list))
                    name = str(img_name) + '-' + str(collect) + '-'+ str(like) + '@' + str(up_name) + '-' + str(i)
                    # os.system('wget %s -q -O dd/{}'.format(name) % img_src)
                    urllib.request.urlretrieve(img_src,'D:/bili/{}.jpg'.format(name)) #手动创建D盘下的bili文件夹
    except:
        print("lost:{}".format(list))
        pass

for i in range(111,384):                                                     #起始页面传入id，b站到18/5大概到3900000                                           
    begin = i*10000
    end = begin + 10000
    urls = ["https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id={}".format(j)
            for j in range(begin, end)]
    with futures.ThreadPoolExecutor(64) as executor:                         #多线程开始
        executor.map(onepage, urls)





