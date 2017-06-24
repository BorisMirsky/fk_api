# coding: utf8

from lxml.html import fromstring, parse
import requests
from requests.exceptions import RequestException
import sys
from collections import OrderedDict
import names


class Make_html:
   def __init__(self, country):                                # принимает по русски
      i = names.country_list_2.index(country)                  # индекс страны
      _country = names.country_list_1[i]     
      self.country = _country 
      self.url = ('http://football.kulichki.net/%s' % self.country)
      self.responce = requests.get(self.url)
      with open('country_page.html', 'w') as output_file:
            output_file.write(self.responce.text) 
      self.html_text = open('country_page.html', 'r').read()

class Citizenship_country:
   def __init__(self, country):
      self.root = Make_html(country)       
      self.make_dict()

# СЛИШКОМ БОЛЬШАЯ ФУНКЦИЯ, НАДО РАЗБИТЬ!
   def make_dict(self):
      tree = fromstring(self.root.html_text)                                  #  html-файл в формате строки - 
      links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')   
      sum_list = []                  # все гражданства страны (сумма гражданств команд страны)
      i=0
      for link in links:           # переход по всем ссылкам - высший дивизион страны
         i+=1
         try:                                   # germany spain italy mls
            responce = requests.get(link)                   #   ----------БУДЕТ МНОГО html-ФАЙЛОВ-!-
            with open('test%d.html' % i, 'w') as output_file:        
               output_file.write(responce.text)                     
            html_text = open('test%d.html' % i, 'r').read()       
         except RequestException:                # turkey england france holland portugal ukraine belarus kz
            responce = requests.get('http://football.kulichki.net' + link)      #   ----------БУДЕТ МНОГО html-ФАЙЛОВ-!-
            with open('test%d.html' % i, 'w') as output_file:       
               output_file.write(responce.text)                     
            html_text = open('test%d.html' % i, 'r').read()                         
         tree = fromstring(html_text)                      # каждую страницу с командой будем парсить
         post = tree.xpath('.//td[@width="15%"]')          # выбираем все гражданства
         keys = []                                         # список гражданств одной команды
         for j in post:                    
            keys.append(j.text_content())                                 
         sum_list.append(keys)                             # сумма списков гражданств всех команд, т.е. гражданства страны
      K=[]                                                 # список списков гражданств
      KK=[]                                                # список кортежей (гражданство, сколько раз)
      for h in sum_list:                                   # надо сделать общий список --КОРЯВЫЙ ВАРИАНТ-!---
         K.extend(h)                                       # список из списков --> общий список
      for l in K:
         zz = K.count(l)                                   # l - страна, zz - сколько раз встречается
         KK.append((l,zz))
      KKK = set(KK)                     # перевод в множество, т.е только. уникальные гражданства
      dd = dict(KKK)                    # перевод в словарь
      y1 = OrderedDict(sorted(dd.items(), key=lambda t: t[1], reverse = True))    
      y = str(list(y1.items()))
      return y

   
   def __repr__(self):
      return(self.make_dict())

