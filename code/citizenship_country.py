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


    def make_dict(self):
        tree = fromstring(self.root) 
        links = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')   
        sum_list = []            
        i=0
        for link in links:     
            i+=1
            try:                          
                time.sleep(1)
                responce = requests.get(link, headers = random_user_agent())     
            except RequestException:   
                time.sleep(1)
                responce = requests.get('http://football.kulichki.net' + link, headers = random_user_agent())
            root = responce.text    
            tree = fromstring(root)                     
            post = tree.xpath('.//td[@width="15%"]')    
            keys = []                                    
            for j in post:                    
                keys.append(j.text_content())                                 
            sum_list.append(keys)        
        K=[]                                                
        KK=[]                                           
        for h in sum_list:                              
            K.extend(h)                            
        for l in K:
            zz = K.count(l)                           
            KK.append((l,zz))
        KKK = set(KK)                    
        dd = dict(KKK)                   
        y1 = OrderedDict(sorted(dd.items(), key=lambda t: t[1], reverse = True))    
        y = list(y1.items())
        res = '\n'.join([(q[0] + ' - ' + str(q[1])) for q in y])
        return res  

   
    def __repr__(self):
        return(self.make_dict())
