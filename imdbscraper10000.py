import pandas as pd 
import numpy as np
import requests
from bs4 import BeautifulSoup

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
           'Accept-Language': 'en-US, en;q=0.5'})

movie_name=[]
year=[]
time=[]
rating=[]
metascore=[]
director=[]
votes=[]
gross=[]
description=[]
genre=[]
cast=[]
cas=[]
pages=np.arange(1,201)

for page in pages:
    url = "https://www.imdb.com/search/title/?num_votes=10000,&sort=user_rating,desc&title_type=feature&start=" + str((page-1)*50 + 1)
    page=requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text,'html.parser')
    movie_data=soup.findAll('div',attrs={'class': 'lister-item mode-advanced'})
    for store in movie_data:
        name=store.h3.a.text
        movie_name.append(name)

        year_of_release=store.h3.find('span',class_="lister-item-year text-muted unbold").text.replace('(','')
        year_of_release=year_of_release.replace(')','')
        year.append(year_of_release)


        gen = store.p.find('span', class_ = "genre").text if store.find('span', class_ = "genre") else "NA"
        genre.append(gen)

        rate=store.find('div',class_="inline-block ratings-imdb-rating").text.replace('\n','') if store.find('div',class_="inline-block ratings-imdb-rating") else "NA"
        rating.append(rate)

        meta = store.find('span',class_="metascore").text if store.find('span',class_="metascore") else "NA"
        metascore.append(meta)

        dire=store.find('p',class_='').find_all('a')[0].text
        director.append(dire)

        cast.append([a.text for a in store.find('p',class_='').find_all('a')[1:]])

        value = store.find_all('span', attrs = {'name':'nv'}) if store.find_all('span', attrs = {'name':'nv'}) else 'NA'
        vote = value[0].text if store.find_all('span', attrs = {'name':'nv'}) else 'NA'

        votes.append(vote)
        
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else 'NA'
        description.append(description_)

for i in cast:
    c=','.join(map(str,i))
    cas.append(c)

movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Genre":genre,"Movie Rating": rating, "Metascore of movie": metascore,"Director":director,"Cast":cas,"Votes" : votes,"Description": description})
movie_list.to_csv("imdbnewdata.csv")