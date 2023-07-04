# coding: utf8
from lxml.html import fromstring
import requests
from collections import OrderedDict
from parse_html import parse_html_country_season, parse_html_country_season_team, season_to_year, one_season_countrys



class Citizenship_team:                   
    def __init__(self, country, season, team):                       
        responce = parse_html_country_season_team(country, season, team)                                         # ?
        tree = fromstring(responce.text) 
        post = tree.xpath('.//td[@width="15%"]')        
        keys = []                                    
        for item in post:
            content = item.text_content()
            keys.append(content)
        values = [keys.count(player) for player in keys]
        self.my_dict = dict(zip(keys, values))

    def make_dict(self):
        res = OrderedDict(sorted(self.my_dict.items(), key=lambda t: t[1], reverse = True))
        res1 = list(res.items())
        res2 = '\n'.join([(q[0] + ' - ' + str(q[1])) for q in res1])
        return res2

    def date_for_plot(self):
        x = self.my_dict
        y =  [i[0] for i in x.items()]             
        z = [i[1] for i in x.items()]         
        return y, z

