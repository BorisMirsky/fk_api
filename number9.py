# coding: utf8
from   lxml.html import fromstring, parse
import requests
import sys
import names
import pandas as pd
from datetime import datetime
import random
import codecs


#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
dateTimeObj = datetime.now()
current_year = dateTimeObj.year

user_agent_file = open("user-agents.txt", "r").readlines()

def random_user_agent():
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header


   
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
         
# Все № страны. Принимает страну по английски
class Make_html_1:
   def __init__(self, country):                                # принимает по русски
      #i = names.country_list[country] #.index(country)                  # индекс страны
      #_country = names.country_list_1[i]
      self.country = get_key(names.country_list, country)       # страна для урла (по английски)
      #self.country = _country                                  
      #self.url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
      self.url = 'https://football.kulichki.net/%s' % (country)
      #self.url = ('http://football.kulichki.net/%s' % self.country)
      self.responce = requests.get(self.url, headers = random_user_agent())
      #self.responce.encoding='utf-8'
      with open('country_page1.html', 'w') as output_file:
          output_file.write(self.responce.text) 
      self.html_text = open('country_page1.html', 'r').read()



class Make_html_2:
    def __init__(self, country):                                # принимает по русски
      #i = names.country_list_2.index(country)                  # индекс страны
      #_country = names.country_list_1[i]                       #  переключает на английский
       # country_lat = names.country_list[country_ru]
        #self.country = country 
        self.url = 'http://football.kulichki.net/%s/%d/' % (country, current_year)
        self.responce = requests.get(self.url, headers = random_user_agent())
        self.responce.encoding='utf-8'
        with open('country_page.html', 'w') as output_file:
            output_file.write(self.responce.text) 
        #self.html_text = open('country_page.html', 'r').read()
        self.html_text = open('country_page.html', 'r').read()
        self.html_text.encode('utf8')

      
# Все 'девятки' чемпионата
class Get_9s:
    def __init__(self, country):
        self.root = Make_html_2(country)       
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
            sum_list.append( df[df['№'] == '9'][["Игрок", 'Гражданство']] )
            return sum_list




# Страна\клуб - выбор одного №.  Принимает страну и клуб по английски
#with open('path\to\file.html', mode='w', encoding='utf-8') as page_file:
#    page_file.write(raw_html)

class Get_9:
   def __init__(self, country, team):
      self.url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
      #self.extract_9()

   def extract_9(self):
      df = pd.read_html(self.url)[1]
      df.columns = ['№', "Игрок", 2, 'Гражданство', 4, 5, 6, 7]
      df.set_index("Игрок")
      x = df[df['№'] == '9'][["Игрок", 'Гражданство']]
      return x #.encode('utf8')



#x = Get_9s('italy') 
#print(x.extract_9s())


#x = Get_9('italy', 'roma')
#print(x.extract_9())


   
