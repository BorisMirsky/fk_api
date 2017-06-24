# coding: utf8

from lxml.html import fromstring, parse
import requests
from collections import OrderedDict

# сохраняет html-страницу для парсинга
class Make_html_team:
   def __init__(self, country, team):
      self.url = 'http://football.kulichki.net/%s/2017/teams/%s.htm' % (country, team)
      self.responce = requests.get(self.url)
      with open('test_1.html', 'w') as output_file:
         output_file.write(self.responce.text) 
      self.html_text = open('test_1.html', 'r').read()

# подсчёт гражданства по игрокам в заданной команде
class Citizenship_team:                       
   def __init__(self, country, team):
      self.root = Make_html_team(country, team)
      tree = fromstring(self.root.html_text)  
      post = tree.xpath('.//td[@width="15%"]')
      keys = []                                           # список гражданств команды
      for i in post:
          z = i.text_content()
          keys.append(z)
      values = [keys.count(h) for h in keys]
      self.d = dict(zip(keys, values))

   def make_dict(self):
      y1 = OrderedDict(sorted(self.d.items(), key=lambda t: t[1], reverse = True))
      y = list(y1.items())
      return y
   
   def date_for_plot(self):
      y = self.d
      z =  [i[0] for i in y.items()]         # список стран, X,             x.date_for_plot()[0]
      zz = [i[1] for i in y.items()]         # список гражданств, L,        x.date_for_plot()[1]
      return z, zz
