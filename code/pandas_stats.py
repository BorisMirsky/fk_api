# coding: utf8
import pandas as pd
import requests
from datetime import datetime
import html5lib
import random
from parse_html import parse_html_country_season_team


class Stats_of_club:
    def __init__(self, country, season, team):
        response = parse_html_country_season_team(country, season, team) 
        self.df = pd.read_html(response.text)[1] 
        self.df.columns = ['№', "Игроки", 2, 3, "Матчи", "Голы", "Жёлтые", "Красные" ]
        self.df = self.df.set_index("Игроки") 

    pd.options.display.float_format = '{:,.0f}'.format   # 5.0  ->  5
    
    def matches(self):
        self.df["Матчи"] = pd.to_numeric(self.df["Матчи"], errors='coerce')
        y = self.df.loc[:,["Матчи"]].sort_values("Матчи", ascending=False)[:5]
        return y

    def goals(self):
        self.df["Голы"] = pd.to_numeric(self.df["Голы"], errors='coerce')
        y = self.df.loc[:,["Голы"]].sort_values("Голы", ascending=False)[:5]  
        return y

    def yellow_red(self):
        self.df["Жёлтые"] = pd.to_numeric(self.df["Жёлтые"], errors='coerce')
        y = self.df.loc[:,["Жёлтые", "Красные"]].sort_values("Жёлтые", ascending=False)[:5]
        return y
