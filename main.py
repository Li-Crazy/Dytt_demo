'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/4/14 15:40
@Software: PyCharm
@File    : main.py
'''
from lxml import etree
import requests

BASE_DOMAIN = "http://www.ygdy8.net"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ('
                  'KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 '
                  'Core/1.70.3650.400 QQBrowser/10.4.3341.400',
    'Referer': 'http://www.ygdy8.net/html/gndy/dyzz/list_23_2.html'
}

def get_detail_urls(url):
    response = requests.get(url,headers=HEADERS)
    # print(response.content.decode('gbk'))
    # with open('dytt.html','w') as f:
    #     f.write(response.content.decode('gbk'))
    text = response.content.decode('gbk')
    parser = etree.HTMLParser(encoding='gbk')
    html = etree.HTML(text,parser=parser)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

    #相当于map()
    # def abx(url):
    #     return BASE_DOMAIN+url
    # index = 0
    # for detail_url in detail_urls:
    #     detail_url = abs(detail_url)
    #     detail_urls[index]=detail_url
    #     index += 1

def parse_detail_page(url):
    response = requests.get(url, headers=HEADERS)
    # print(response.content.decode('gbk'))
    text = response.content.decode('gbk')
    parser = etree.HTMLParser(encoding='gbk')
    html = etree.HTML(text, parser=parser)
    title = html.xpath("//div[@class='title_all']//font/text()")[0]
    ZoomE = html.xpath("//div[@id='Zoom']")[0]
    imgs = ZoomE.xpath(".//img/@src")
    cover = imgs[0]
    screenshot = imgs[1]
    movie = {
        "title":title,
        "cover":cover,
        "screenshot":screenshot,
    }
    def parse_info(info,rule):
        return info.replace(rule,"").strip()#replace()字符串替换,# .strip删除前后空白

    infos = ZoomE.xpath(".//text()")
    for index,info in enumerate(infos):#enumerate返回列表索引和对应元素
        if info.startswith("◎年　　代"):#startswirh(str)字符串是否以str开头
            info = parse_info(info,"◎年　　代")
            movie['year']=info
        elif info.startswith("◎产　　地"):
            info = parse_info(info,"◎产　　地")
            movie["country"]=info
        elif info.startswith("◎类　　别"):
            info = parse_info(info,"◎类　　别")
            movie["category"] = info
        elif info.startswith("◎语　　言"):
            info = parse_info(info,"◎语　　言",)
            movie["language"] = info
        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info,"◎豆瓣评分")
            movie["douban_rating"] = info
        elif info.startswith("◎片　　长"):
            info = parse_info(info,"◎片　　长")
            movie["duration"] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info,"◎导　　演")
            movie["director"] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info,"◎主　　演")
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie["actor"] = actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info,"◎简　　介")
            for x in range(index+1,len(infos)):
                profile = infos[x].strip()
                if profile.startswith("【下载地址】"):
                    break
                elif profile.startswith("◎获奖情况"):
                    break
                else:
                    movie["profile"] = profile
                # print(profile)
                # print(movie)

    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")
    movie['download_url'] = download_url
    print(download_url)
    return movie

def spider():
    base_url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html"
    movies = []
    for x in range(1,8):
        url = base_url.format(x)
        # print(url)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)
        # print(movies)

if __name__ == '__main__':
    spider()