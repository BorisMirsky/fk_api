# coding: utf8
from lxml.html import fromstring
import names
from Parse_html import parse_html_country_season, parse_html_country_season_team, season_to_year, one_season_countrys




class Teams:
    def __init__(self, country_ru, season):
        country_lat = names.country_list[country_ru]
        #year = season_to_year(country_lat, season)
        #self.response = parse_html_country(country_lat)
        self.response = parse_html_country_season(country_lat, season)

    def get_teams(self):
        tree = fromstring(self.response.text) 
        post = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a')
        teams = [i.text_content() for i in post]
        teams.insert(0, "")     
        return teams               
   
    def __repr__(self):
        return str(self.get_teams())


#x = Teams('Италия', 'Архив 2018/2019') 
#print(x.get_teams())

