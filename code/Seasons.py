# coding: utf8
from lxml.html import fromstring
import names
from Parse_html import parse_html_country_season 
from datetime import datetime


dateTimeObj = datetime.now()
current_year = dateTimeObj.year

class Seasons:
    def __init__(self, country_ru):
        country_lat = names.country_list[country_ru]
        self.response = parse_html_country_season(country_lat, current_year)
        self.country_ru = country_ru
                    

    def get_seasons(self):
        tree = fromstring(self.response.text)
        if self.country_ru == "Голландия":                 # У чемпионата Нидерландов сбита верстка
            n = '4'
        else:
            n = '3'
        post = tree.xpath('.//li[@class="yellow-green-bg"][{0}]/ul/li/a'.format(n))
        seasons = [i.text_content() for i in post]
        seasons[0:0] = '', 'Текущий сезон'
        #seasons[0] = 'Текущий сезон'
        return seasons          
  
    def __repr__(self):
        return str(self.make_dict())


#x = Seasons('Франция') 
#print(x.get_seasons())

