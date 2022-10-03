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

def random_user_agent():
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header

def parse_html_country_year_team(country, team):
    url = 'https://football.kulichki.net/%s/%d/teams/%s.htm' % (country, current_year, team)
    response = requests.get(url, headers = random_user_agent())
    #df = pd.read_html(response.text)[1]      # response.url ---> bad decoding
    return response #df

def parse_html_country(country):
    url = 'http://football.kulichki.net/%s/' % (country) 
    response = requests.get(url, headers = random_user_agent())
    return response


#x = parse_html_country_year_team('italy', 'inter')
#x = parse_html_country('italy')
#print(x)
