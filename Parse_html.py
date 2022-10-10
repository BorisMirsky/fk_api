# coding: utf8
from lxml.html import fromstring 
import requests
import sys
import pandas as pd
from datetime import datetime
import random


dateTimeObj = datetime.now()
current_year = dateTimeObj.year
user_agent_file = open('user-agents.txt', 'r').readlines()
one_season_countrys = ['kz', 'belarus', 'mls']


def random_user_agent():
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header

def season_to_year(country, season):
    year = ""
    if country in one_season_countrys:
        if season == "Текущий сезон":
            year = current_year
        else:
            year = str(season)[-4:]
    else:
        if season == "Текущий сезон":
            year = current_year + 1
        else:
            year = str(season)[-4:]
    return year


def parse_html_country_season_team(country, season, team):
    year = season_to_year(country, season)        
    url = 'https://football.kulichki.net/%s/%s/teams/%s.htm' % (country, year, team)
    response = requests.get(url, headers = random_user_agent())
    return response 


def parse_html_country_season(country, season):
    year = season_to_year(country, season)               
    url = 'http://football.kulichki.net/%s/%s/' % (country, year) 
    response = requests.get(url, headers = random_user_agent())
    return response



#parse_html_country_season('italy', 'Архив 2017/2018')
#parse_html_country_season_team('italy', 'Архив 2017/2018', 'roma')
#season_to_year('france', 'Текущий сезон')

