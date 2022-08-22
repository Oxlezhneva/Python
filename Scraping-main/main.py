import requests
import bs4
import pandas as pd

keywords = ['token', 'разработка', 'web', 'машинное обучение']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}
https = 'https://habr.com'
res = requests.get('https://habr.com/ru/all', headers = HEADERS)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
my_list = []
posts = soup.find_all('article',class_="tm-articles-list__item")
for hubs in posts:
    hub_name = hubs.text.lower()   
    for word in keywords:
        if word in hub_name:
            href = https + hubs.find(class_="tm-article-snippet__title-link").attrs['href']
            date_time = hubs.find(class_="tm-article-snippet__datetime-published").find('time').text
            title = hubs.find("h2").find('span').text
            test = (f'{date_time} - {title} - {href}')  
            my_list.append(test)
            
               
if my_list != []:   
    list_drop_duplicates = pd.Series(my_list).drop_duplicates().tolist()         
    for item in list_drop_duplicates: 
        print(item)
else:
    print('Совпадения по заданным ключевым словам не найдены')
    
