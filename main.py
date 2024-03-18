# Импорт необходимых библиотек
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse
import re
import json

# Путь к странице с данным
website = "https://books.toscrape.com/"

# GET-запрос к серверу
page = requests.get(website)

# Парсинг данных
soup = BeautifulSoup(page.content, 'html.parser')

# Поиск по тегу <li>
result = soup.find_all('li', ('class','col-xs-6 col-sm-4 col-md-3 col-lg-3'))

# Объединение ссылок на книги
# Первая часть ссылки
url_1 = website

# Извлечение списка относительных ссылок на товары
url_2 = []
for i in result:
  url_2.append(i.find('a').get('href'))

# Объединение двух частей ссылки в абсолютный путь и создание списка со ссылками на каждый товар, расположенный на странице
url_joined = []

for link in url_2:
  url_joined.append(urllib.parse.urljoin(url_1, link))

# Пустые списки, которые будут содержать соответствующие данные: название, цена, форма выпуска, содержание, производитель
name_book = []
price = []
qty_availible = []
description = []
output = {}

for i in url_joined:
  response = requests.get(i)
  soup_2 = BeautifulSoup(response.content, 'html.parser')

  # Парсинг названия книги
  try:
    name_book.append(soup_2.find('h1').text)
  except:
    name_book.append('')

  # Парсинг оставшегося количества
  try:
    av = soup_2.find('p', ('class', 'instock availability')).text
    av = int(re.sub(r'[^\d.]+', '', av))
    qty_availible.append(av)
  except:
    qty_availible.append('')

  # Парсинг цены
  try:
    pr = soup_2.find('p', ('class', 'price_color')).text
    pr = float(re.sub(r'[^\d.]+', '', pr))
    price.append(pr)
  except:
    price.append('')

  # Парсинг описания
  try:
    description.append(soup_2.find('h2').find_next().text)
  except:
    description.append('')

  output = {'name_book': name_book, 'price': price, 'in_stock': qty_availible, 'description': description}

df = pd.DataFrame(output)
print(df)

# сохранение данных в JSON-файл
with open('books_toscrape_com.json', 'w') as f:
    json.dump(output, f)