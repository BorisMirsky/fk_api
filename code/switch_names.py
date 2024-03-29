# coding: utf8
from lxml.html import fromstring 
import names
from parse_html import parse_html_country_season, season_to_year


# преобразует клуб с русского на английский
def switch_names(country_ru, team_ru, season):
      country_lat = names.country_list[country_ru]
      year = season_to_year(country_lat, season)
      response = parse_html_country_season(country_lat, year)
      tree = fromstring(response.text)
      # генерит на лету список клубов по английски (вынимает все url'ы)
      post1 = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a/@href')
      teams1 = [i.split('/')[-1] for i in post1]    # разбили адрес по /
      teams11 = [j.split('.')[0] for j in teams1]   # разбили team.htm по точке
      teams11.insert(0, "")     
      # генерит на лету список клубов по русски
      post2 = tree.xpath('.//li[@class="yellow-green-bg"][2]/ul/li/a')
      teams2 = [i.text_content() for i in post2]
      teams2.insert(0, "")     
      # меняем русское название на английское
      j = teams2.index(team_ru)             # индекс клуба в русском списке
      team1 = teams11[j]                    # клуб в английском списке по индексу
      return [country_lat, team1]           # вернёт имена на английском


