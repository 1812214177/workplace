import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pandas

#获取新闻分页的时间标题和网址123
'''
url='http://news.sina.com.cn/china/'
def get_items(url):
    html=requests.get(url)
    html.encoding='utf-8'
    soup=BeautifulSoup(html.text,'lxml')
    for news in soup.select('.news-item'):
        if(len(news.select('h2'))>0):
            h2=news.select('h2')[0].text
            time=news.select('.time')[0].text
            a=news.select('a')[0]['href']
            print(time,h2,a)
'''


#获得新闻正文的详细信息

def get_details(newsurl):

    result={}
    res=requests.get(newsurl)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('#artibody p')[0].text
    result['newssource']=soup.select('.time-source  span a')[0].text
    timesource=soup.select('.time-source')[0].contents[0].strip()
    result['time']=datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['article']=' '.join([p.text.strip()  for  p in soup.select('#artibody p')[:-1]])
    result['editor']=soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['comments']=getCommentCount(newsurl)
    return result

#获取评论数
commentURL='http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
def getCommentCount(newsurl):
    m=re.search('doc-i(.*).shtml',newsurl)
    newsid=m.group(1)
    comments=requests.get(commentURL.format(newsid))
    jd=json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


#print(get_details(newsurl))


def parseListLinks(url):
    newsdetails=[]
    res=requests.get(url)
    jd=json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:

        newsdetails.append(get_details(ent['url']))
    return newsdetails
#获取所有分页中的新闻内容


url='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1503621315925'
news_total=[]
for page in range (1,3):
    newsurl=url.format(page)
    newsary=parseListLinks(newsurl)
    news_total.extend(newsary)

#print(newsary)
df=pandas.DataFrame(news_total)
#print(df.head(10))
df.to_excel('news1.xlsx')
#import sqlite3
#with sqlite3.connect('news.sqlite')as db
    #db.to_sql('news',con=db)