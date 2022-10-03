# coding: utf8
from lxml.html import fromstring
import names
from Parse_html import parse_html_country 


class Teams:
    def __init__(self, country_ru):
        country_lat = names.country_list[country_ru]
        self.response = parse_html_country(country_lat)

    def make_dict(self):
        tree = fromstring(self.response.text) 
        post = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a')
        teams = [i.text_content() for i in post]
        teams.insert(0, "")     
        return teams               
   
    def __repr__(self):
        return str(self.make_dict())


#x = Teams('Италия') 
#print(x.make_dict())

