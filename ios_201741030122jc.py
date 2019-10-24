import requests
from bs4 import BeautifulSoup 

import multiprocessing as mp
import time

t1=time.time()
r = requests.get('https://car.autohome.com.cn/price/list-0-3-0-0-0-0-0-0-0-0-0-0-0-0-0-1.html')

c=r.text

soup=BeautifulSoup(c,'html.parser')
content = soup.find_all('div',{'class':'list-cont'})
print(content)
page_div = soup.find('div',{'class':'page'})
page = page_div.find_all('a')[-2].text
cars= []

urls = ['https://car.autohome.com.cn/price/list-0-3-0-0-0-0-0-0-0-0-0-0-0-0-0-'+str(i)+'.html' for i in range(1,11)]

def crawl_page(url):

    p_r = requests.get(url)
    p_c=p_r.text
    p_soup=BeautifulSoup(p_c,'html.parser')
    p_content = p_soup.find_all('div',{'class':'list-cont'})
    pageCar = []

    for car in p_content:
        carDic = {}
        carDic['picUrl'] = car.find('div',{'class':'list-cont-img'}).find('img')['src']
        carDic['name'] = car.find('div',{'class':'list-cont-main'}).find('a').text
        try:
            carDic['score'] = car.find('span',{'class':'score-number'}).text
        except Exception as e:
            carDic['score'] = ''
        
        pageCar.append(carDic)
    return pageCar  

pool = mp.Pool()
multi_res = [pool.apply_async(crawl_page,(url,)) for url in urls]
pageCars = [res.get() for res in multi_res]

for pageCar in pageCars:
    for car in pageCar:
        cars.append(car)
print(len(cars))
t2= time.time()
print(t2-t1)