# coding: utf8

from lxml.html import fromstring, parse
import requests
from collections import OrderedDict
import datetime
import random


dateTimeObj = datetime.datetime.now() #datetime.now(tz=None)
current_year = dateTimeObj.year

user_agent_file = open("user-agents.txt", "r").readlines()

def random_user_agent():
    #user_agent_file = open("user-agents.txt", "r").readlines()
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header


# сохраняет html-страницу для парсинга
class Make_html_team:
   def __init__(self, country, team):
      url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
      responce = requests.get(url, headers = random_user_agent())
      with open('test_1.html', 'w') as output_file:
         output_file.write(responce.text) 
      self.html_text = open('test_1.html', 'r').read()



# Citizenship_team(x1, x2)
# подсчёт гражданства по игрокам в заданной команде
class Citizenship_team:                       
   def __init__(self, country, team):
      root = Make_html_team(country, team)
      tree = fromstring(root.html_text)  
      post = tree.xpath('.//td[@width="15%"]')
      keys = []                                           # список гражданств команды
      for i in post:
          z = i.text_content()
          keys.append(z)
      values = [keys.count(h) for h in keys]
      self.my_dict = dict(zip(keys, values))

   def make_dict(self):
      y1 = OrderedDict(sorted(self.my_dict.items(), key=lambda t: t[1], reverse = True))
      y = list(y1.items())
      res = '\n'.join([(q[0] + ' - ' + str(q[1])) for q in y])
      return res
   
   def date_for_plot(self):
      y = self.my_dict
      z =  [i[0] for i in y.items()]         # список стран, X,             x.date_for_plot()[0]      
      zz = [i[1] for i in y.items()]         # список гражданств, L,        x.date_for_plot()[1]
      return z, zz


#x = Citizenship_team('holland', 'az')
#print(x.make_dict())

   
