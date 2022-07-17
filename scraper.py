import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from itertools import zip_longest

url = 'https://www.citilink.ru/catalog/noutbuki/'
i = 0

id_lst = []
titles_lst = []
prices_lst = []
promo_prices_lst = []
links_lst = []



while i < 20:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    url = soup.find('a', class_='js--PaginationWidget__page PaginationWidget__arrow js--PaginationWidget__arrow PaginationWidget__arrow_right')
    url = url.get('href')
    names = soup.find_all('div', class_='ProductCardVertical__description')
    prices = soup.find_all('span', class_='ProductCardVerticalPrice__price-current_current-price js--ProductCardVerticalPrice__price-current_current-price')
    promo_prices = soup.find_all('span', class_='ProductCardVerticalPrice__price-club_current-price js--ProductCardVerticalPrice__price-club_current-price')

    for name in names:
        titles_lst.append(name.text)
    for p in prices:
            prices_lst.append(p.text)

    new_prices_lst = prices_lst[::2]
    for pr in promo_prices:
        promo_prices_lst.append(pr.text)

    new_promo_prices_lst = promo_prices_lst[::2]

    substring = 'https://www.citilink.ru/product'

    for l in soup.find_all('a'):
        if type(l.get('href')) is str:
            if substring in l.get('href'):
                link = l.get('href').replace('otzyvy/', '')
                product_id = link[-8:-1]
                id_lst.append(product_id)
                links_lst.append(link)

    i+=1


d = [id_lst, titles_lst, new_prices_lst, new_promo_prices_lst, links_lst]
export_data = zip_longest(*d, fillvalue = '')
with open('notуbooks.csv', 'w', encoding='utf8', newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("id", "title", "price", "promo_price", "url"))
      wr.writerows(export_data)
myfile.close()

# data = {'id': id_lst,'title': titles_lst,'price': prices_lst,'promo_price': promo_prices_lst,'url': links_lst}
# df = pd.DataFrame(data)
# print(df)