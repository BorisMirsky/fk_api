# coding: utf8

from lxml.html import fromstring, parse
import requests
from requests.exceptions import RequestException
import sys
from collections import OrderedDict
import names
import random
import time


user_agent_file = open("../user-agents.txt", "r").readlines()

def random_user_agent():
    random_user_agent = random.choice(user_agent_file).strip()
    header = {'user-agent': random_user_agent}
    return header



class Citizenship_country:
    def __init__(self, country_ru):
        country = names.country_list[country_ru] 
        url = ('http://football.kulichki.net/%s' % country)
        responce = requests.get(url, headers = random_user_agent())
        self.root = responce.text


# СЛИШКОМ БОЛЬШАЯ ФУНКЦИЯ, НАДО РАЗБИТЬ!
# плохие переменный, плохо называются
    def make_dict(self):
        tree = fromstring(self.root) 
        links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')   
        sum_list = []                # все гражданства страны (сумма гражданств команд страны)
        i=0
        for link in links:           # переход по всем ссылкам - высший дивизион страны
            i+=1
            try:                          
                time.sleep(1)
                responce = requests.get(link, headers = random_user_agent())     
            except RequestException:   
                time.sleep(1)
                responce = requests.get('http://football.kulichki.net' + link, headers = random_user_agent())

            root = responce.text    
            tree = fromstring(root)                           # каждую страницу с командой будем парсить
            post = tree.xpath('.//td[@width="15%"]')          # выбираем все гражданства
            keys = []                                         # список гражданств одной команды
            for j in post:                    
                keys.append(j.text_content())                                 
            sum_list.append(keys)                             # сумма списков гражданств всех команд, т.е. гражданства страны
        K=[]                                                 # список списков гражданств
        KK=[]                                                # список кортежей (гражданство, сколько раз)
        for h in sum_list:                                   # надо сделать общий список --КОРЯВЫЙ ВАРИАНТ-!---
            K.extend(h)                                       # список из списков --> общий список
        for l in K:
            zz = K.count(l)                                   # l - страна, zz - сколько раз встречается
            KK.append((l,zz))
        KKK = set(KK)                     # перевод в множество, т.е только. уникальные гражданства
        dd = dict(KKK)                    # перевод в словарь
        y1 = OrderedDict(sorted(dd.items(), key=lambda t: t[1], reverse = True))    
        y = list(y1.items())
        res = '\n'.join([(q[0] + ' - ' + str(q[1])) for q in y])
        return res  

   
    def __repr__(self):
        return(self.make_dict())


#x = Citizenship_country("Украина")
#print(x)
