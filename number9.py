# coding: utf8

import requests
from lxml import html
import pandas as pd
from Parse_html import parse_html_country_year_team, parse_html_country, random_user_agent
import os

def func_get9(country, team):
    response = parse_html_country_year_team(country, team)
    df = pd.read_html(response.text)[1] 
    df.columns = ['№', 'Игрок', 'Дата рождения', 'Гражданство', 4, 5, 6, 7]
    df = df.set_index('Игрок')    
    y = df.loc[df['№'] == '9'][['Гражданство','Дата рождения']]
    return y

#x = func_get9('italy', 'inter')
#print(x)


def func_get9s(country):
    responce = parse_html_country(country)
    tree = html.fromstring(responce.content)                                  
    links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')  
    sum_list = []                                                           
    for link in links:        
        responce = requests.get('http://football.kulichki.net' + link, headers = random_user_agent())
        df = pd.read_html(responce.text, header=None)[1]
        df.columns = ['№', "Игрок", "Дата рождения", 'Гражданство', 4, 5, 6, 7]
        df = df.set_index('Игрок')          # назначаю "Игрок" индексом
        res = df[df['№'] == '9'][['Гражданство', "Дата рождения"]]
        sum_list.append(res.astype(str))
        #print(os.path.basename(link).split('.')[0])
    return sum_list

#w = func_get9('italy', 'roma') 
#print(w)
