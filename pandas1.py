# coding: utf8
import pandas as pd
import requests
from datetime import datetime
#import html5lib



dateTimeObj = datetime.now()
current_year = dateTimeObj.year

# принимает страну и клуб, строит урл, строит таблицу из страницы
class Do_pandas:                       
   def __init__(self, country, team):
      #https://football.kulichki.net/france/2023/teams/reims.htm
      url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
      r = requests.get(url)                   # ?
      self.df = pd.read_html(r.text)[1]       # ?     
      self.df.columns = ['№', "Игроки", 2, 3, "Матчи", "Голы", "Жёлтые", "Красные" ]
      self.df = self.df.set_index("Игроки") # назначаю "Игроков" индексом
          
   def matches(self):
      # для сортировки меняется тип столбца на цифровой
      self.df["Матчи"] = pd.to_numeric(self.df["Матчи"], errors='coerce')
      # сортировка по убыванию
      y = self.df.loc[:,["Матчи"]].sort_values("Матчи", ascending=False)[:5]   # 5 верхних результатов
      return y

   def goals(self):
      self.df["Голы"] = pd.to_numeric(self.df["Голы"], errors='coerce')
      y = self.df.loc[:,["Голы"]].sort_values("Голы", ascending=False)[:5]
      return y

   def yellow_red(self):
      self.df["Жёлтые"] = pd.to_numeric(self.df["Жёлтые"], errors='coerce')
      y = self.df.loc[:,["Жёлтые", "Красные"]].sort_values("Жёлтые", ascending=False)[:5]
      return y

   # не используется ("красные" есть в "жёлтых")
   #def red(self):       
   #   self.df["Красные"] = pd.to_numeric(self.df["Красные"], errors='coerce')
   #   y = self.df.loc[:,["Красные"]].sort_values("Красные", ascending=False)[:5]
   #   return y


#x = Do_pandas('italy', 'roma')
#print(x.yellow_red())
