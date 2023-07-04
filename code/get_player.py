# coding: utf8
import requests
from lxml import html
import pandas as pd
from parse_html import parse_html_country_season_team, parse_html_country_season, random_user_agent
import os


# получить игрока под заданным номером из [чемпионат, сезон, команда]
# Например: "за Ливерпуль 3 года назад бегал хороший левый край под №5, забыл как его звали"
def get_number_player(country, season, team, number):
    response = parse_html_country_season_team(country, season, team) 
    df = pd.read_html(response.text)[1] 
    df.columns = ['№', 'Игрок', 'Дата рождения', 'Гражданство', 4, 5, 6, 7]
    res = ""
    if number in df['№'].tolist():
        df = df.set_index('Игрок')    
        res = df.loc[df['№'] == number][['Гражданство','Дата рождения']]
        res.columns = [''] * len(res.columns)
        res.index.name = None
        return res
    else:
        res = 'В команде {0} нет игрока под № {1}'.format(team, number)
        return res

