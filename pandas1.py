# coding: utf8
import pandas as pd


# принимает страну и клуб, строит урл, строит таблицу из страницы
class Do_pandas:                       
   def __init__(self, country, team):
      url = 'http://football.kulichki.net/%s/2017/teams/%s.htm' % (country, team)
      self.df = pd.read_html(url)[1]            
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
   
   def red(self):       # не используется ("красные" есть в "жёлтых")
      self.df["Красные"] = pd.to_numeric(self.df["Красные"], errors='coerce')
      y = self.df.loc[:,["Красные"]].sort_values("Красные", ascending=False)[:5]
      return y


# x = Do_pandas('italy', 'napoli')
