# coding: utf8
# Примет страну по русски, переключит её на английский,
#               пропарсит, вернёт список клубов по русски. 


from lxml.html import fromstring, parse
import requests
import names
import random





user_agent_file = open("user-agents.txt", "r").readlines()

def random_user_agent():
    #user_agent_file = open("user-agents.txt", "r").readlines()
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header

   
class Make_team:
   def __init__(self, country_ru):                                # примет страну по русски
    #  self.country = country
    #  i = names.country_list_2.index(country)                  # индекс страны
    #  _country = names.country_list_1[i]                       # страна по английски
      country_lat = names.country_list[country_ru]
      self.url = 'http://football.kulichki.net/%s/' % (country_lat) #_country)
      self.responce = requests.get(self.url, headers = random_user_agent())
      with open('_test_1.html', 'w') as output_file:
         output_file.write(self.responce.text) 
      self.html_text = open('_test_1.html', 'r').read()

class Teams:
   def __init__(self, country):
      self.root = Make_team(country)
      self.make_dict()

   def make_dict(self):
      tree = fromstring(self.root.html_text)
     # post = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')
     # teams1 = [i.split('/')[-1] for i in post]   # разбили адрес по /
     # teams = [j.split('.')[0] for j in teams1]   # разбили team.htm по точке
      post = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a')
      teams = [i.text_content() for i in post]
      #teams.insert(0, "   ")  # ?
      return teams   # вернёт список клубов
   
   def __repr__(self):
      return str(self.make_dict())


#x = Teams('Казахстан')  #Make_team('Франция')
#print(x) #.make_dict())
#x.__repr__()
#print(list(names.country_list.keys()))


