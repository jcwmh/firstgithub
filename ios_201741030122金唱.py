import requests
from bs4 import BeautifulSoup 

import multiprocessing as mp
import time

t1=time.time()
r = requests.get('https://b.faloo.com/y/0/0/0/4/2/0/1.html')

n=r.text

soup=BeautifulSoup(n,'html.parser')
#content = soup.find_all('div',{'class':'list-cont'})

page_div = soup.find('div',{'class':'l_page'})
#print(page_div)
page=page_div.find_all('a')[-2].text
novels=[]

urls = ['https://b.faloo.com/y/0/0/0/4/2/0/'+str(i)+'.html' for i in range(1,31)]

def crawl_page(url):

    p_r = requests.get(url)
    p_n=p_r.text
    p_soup=BeautifulSoup(p_n,'html.parser')
    p_content = p_soup.find_all('div',{'class':'l_bar'})
    pageNovel= []

    for novel in p_content:
        novelDic = {}
        novelDic['picUrl'] = novel.find('div',{'class':'l_pic'}).find('img')['src']
        novelDic['name'] = novel.find('div',{'class':'l_rc'}).find('a').text        
        
        pageNovel.append(novelDic)
    return pageNovel  

pool = mp.Pool()
multi_res = [pool.apply_async(crawl_page,(url,)) for url in urls]
pageNovels = [res.get() for res in multi_res]

for pageNovel in pageNovels:
    for novel in pageNovel:
        novels.append(novel)
print(len(novels))
t2= time.time()
print(t2-t1)
