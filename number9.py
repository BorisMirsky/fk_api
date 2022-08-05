# coding: utf8
from   lxml.html import fromstring, parse
import requests
import sys
import names
import pandas as pd
from datetime import datetime




dateTimeObj = datetime.now()
current_year = dateTimeObj.year

# Все № страны. Принимает страну по английски
class Make_html_1:
   def __init__(self, country):                                # принимает по русски
      i = names.country_list_2.index(country)                  # индекс страны
      _country = names.country_list_1[i]                       
      self.country = _country                                  # страна для урла (по английски)
      self.url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
      #self.url = ('http://football.kulichki.net/%s' % self.country)
      self.responce = requests.get(self.url)
      with open('country_page1.html', 'w') as output_file:
            output_file.write(self.responce.text) 
      self.html_text = open('country_page1.html', 'r').read()

class Get_9s:
   def __init__(self, country):
      self.root = Make_html_1(country)       
      self.extract_9s()

   def extract_9s(self):
      tree = fromstring(self.root.html_text)                                   #  html-файл в формате строки - 
      links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')   # колонка со всеми клубами
      sum_list = []                                                            # пустой список 
      i=0
# link (= url) - отдельная страница каждого клуба 
      for link in links:           # переход по всем ссылкам - высший дивизион страны
         df = pd.read_html(link)[1]
         df.columns = ['№', "Игрок", 2, 'Гражданство', 4, 5, 6, 7]
         df.set_index("Игрок")
         return df[df['№'] == '9'][["Игрок", 'Гражданство']]


# Страна\клуб - выбор одного №.  Принимает страну и клуб по английски
class Get_9:
   def __init__(self, country, team):
      self.url = 'http://football.kulichki.net/%s/2017/teams/%s.htm' % (country, team)
      self.extract_9()

   def extract_9(self):
      df = pd.read_html(self.url)[1]
      df.columns = ['№', "Игрок", 2, 'Гражданство', 4, 5, 6, 7]
      df.set_index("Игрок")
      x = df[df['№'] == '9'][["Игрок", 'Гражданство']]
      return x



#x = Get_9('italy', 'napoli')
#print(x.extract_9())

   
