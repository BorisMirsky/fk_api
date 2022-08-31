# coding: utf8
# примет страну и клуб по русски ('пользовательский вид'),
#          вернёт их же на английском ('технический вид' для url'а)


from lxml.html import fromstring, parse
import requests
import names
import random
from datetime import datetime



dateTimeObj = datetime.now()
current_year = dateTimeObj.year

user_agent_file = open("user-agents.txt", "r").readlines()     # 1000 ua

def random_user_agent():
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header
   

class Make_page:
   def __init__(self, country_ru, team_r):               # примет страну по русски
      # преобразует страну с русского на английский       
      #i = names.country_list_2.index(country_r)         # индекс страны
      country = names.country_list[country_ru]                 # страна по английски
      # построит url страны, сохранит страницу    
      self.url1 = 'http://football.kulichki.net/%s/' % (country)
      self.responce = requests.get(self.url1, headers = random_user_agent())
      with open('_test_2.html', 'w') as output_file:
         output_file.write(self.responce.text) 
      self.html_text = open('_test_2.html', 'r').read()


class Country_team:
   def __init__(self, country_r, team_r):
      self.root = Make_page(country_r, team_r)    # сохранённая html-страница
      self.team = team_r                          # клуб по русски
      # преобразует страну с русского на английский  - ещё раз
      #i = names.country_list_2.index(country_r)       # индекс страны
      self.country = names.country_list[country_r]          # страна по английски
      self.switch_names()                         

   # преобразует клуб с русского на английский
   def switch_names(self):
      tree = fromstring(self.root.html_text)     # дерево для парсинга   
      # генерит на лету список клубов по английски (вынимает все url'ы)
      post1 = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')
      teams1 = [i.split('/')[-1] for i in post1]    # разбили адрес по /
      teams11 = [j.split('.')[0] for j in teams1]   # разбили team.htm по точке
      teams11.insert(0, "")     
      # генерит на лету список клубов по русски
      post2 = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a')
      teams2 = [i.text_content() for i in post2]
      teams2.insert(0, "")     
      # меняем русское название на английское
      j = teams2.index(self.team) #!        # индекс клуба в русском списке
      team1 = teams11[j]                    # клуб в английском списке по индексу
      return self.country, team1            # вернёт имена на английском
        
   def __repr__(self):
      return str(self.switch_names())



#x = Country_team('Англия','Лидс')
#print(x.switch_names())
