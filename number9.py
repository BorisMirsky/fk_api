# coding: utf8

import requests
from lxml import html
import pandas as pd
from Parse_html import parse_html_country_season_team, parse_html_country_season, random_user_agent
import os



def func_get9(country, team, number):
    response = parse_html_country_season_team(country, team)   
    tree = html.fromstring(response.content)
    clubname = tree.xpath('.//font[@size="6"]/text()')[0]
    print(str(clubname))
    # etree.tostring(child, method="html", encoding="unicode")
    df = pd.read_html(response.text)[1] 
    df.columns = ['№', 'Игрок', 'Дата рождения', 'Гражданство', 4, 5, 6, 7]
    if number in df['№'].tolist():
        df = df.set_index('Игрок')    
        res = df.loc[df['№'] == number][['Гражданство','Дата рождения']]
        res.columns = [''] * len(res.columns)
        res.index.name = None
        return res
    else:
        res = 'В команде {0} нет игрока под № {1}'.format(clubname, number)
        return res
    

#x = func_get9('italy', 'torino', '57')
#print(x)


def func_get9s(country, number):
    responce = parse_html_country_season(country)
    tree = html.fromstring(responce.content)                                  
    links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')  
    sum_list = []                                                           
    for link in links:        
        responce = requests.get('http://football.kulichki.net' + link, headers = random_user_agent())
        tree = html.fromstring(responce.content)
        clubname = tree.xpath('.//font[@size="6"]/text()')[0]
        df = pd.read_html(responce.text, header=None)[1]
        df.columns = ['№', "Игрок", "Дата рождения", 'Гражданство', 4, 5, 6, 7]
        if number in df['№'].tolist():
            df = df.set_index('Игрок')    
            res = df.loc[df['№'] == number][['Гражданство','Дата рождения']]
            res.columns = [''] * len(res.columns)
            res.index.name = None
            sum_list.append(res.astype(str))
        else:
            res = 'В команде {0} нет игрока под № {1}'.format(clubname, number)
            sum_list.append(res)
    return sum_list

#w = func_get9s('france', '12') 
#print(w)
