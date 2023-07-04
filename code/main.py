# coding: utf8

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import time
# from the same project
from get_player import get_number_player
import names
from teams import Teams                                
from seasons import Seasons                             
from switch_names import switch_names                   
from citizenship_team import Citizenship_team           
from citizenship_country import Citizenship_country    
from pandas_stats import Stats_of_club                 
                                                        
                 
font = {'family': 'DejaVu Sans','weight': 'normal'}     # шрифт для Ubuntu 
rc('font', **font)                                      # ---//---


class MainDialog(QDialog):  
    def __init__(self, fileName, parent=None):
        super(MainDialog, self).__init__(parent)  
        fileInfo = QFileInfo(fileName)          
        tabWidget = QTabWidget()  
        tabWidget.addTab(Tab1(fileInfo), "Tab1")
        tabWidget.addTab(Tab2(fileInfo), "Tab2")
        tabWidget.addTab(Tab3(fileInfo), "Tab3")
        tabWidget.addTab(Tab4(fileInfo), "Tab4")
        tabWidget.addTab(Tab5(fileInfo), "Tab5")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addStretch(0)
        self.setLayout(mainLayout)
        self.setWindowTitle("API for football.kulichki")
        self.setWindowIcon(QIcon('../static/tshirt_icon.png'))     
        self.resize(300, 650)                               
        self.move(150, 150)
        self.sshFile="../static/darkorange.stylesheet"   # Внешний файл с таблицей стилей взят здесь:
        with open(self.sshFile,"r") as fh:               # http://www.yasinuludag.com/darkorange.stylesheet
            self.setStyleSheet(fh.read())


class Tab1(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab1, self).__init__(parent)
        label1 = QLabel('Сайт "Футбол на Куличках" \nпопулярен'
                          ' как удобный и достоверный\n источник статистических данных о футболе.'
                           '\n\nЭта программа '
                          'обрабатывает\nнекоторые параметры команд и игроков.\n'
                          'Используются внешние парсеры, matplotlib, pandas.\n'
                          'Все данные создаются динамически.')
        layout = QVBoxLayout()
        layout.addWidget(label1)
        self.setLayout(layout)

      
class Tab2(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab2, self).__init__(parent)
        self.label1 = QLabel('Выбор страны')
        self.countries_ru_list = QComboBox()                
        self.label2 = QLabel('Выбор сезона')
        self.seasons_list = QComboBox()                         
        self.label_space = QLabel('')
        self.label3 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()                    
        self.label4 = QLabel('Гражданство игроков команды')          
        self.text_field = QPlainTextEdit()                 
        self.text_field.setReadOnly(True)
        self.label5 = QLabel('Получить график') 
        self.btn1 = QPushButton("Get plot", self)
 
        self.countries_ru_list.addItems(list(names.country_list.keys()))
        self.countries_ru_list.currentIndexChanged.connect(self.select_country)   
        self.seasons_list.currentIndexChanged.connect(self.select_season)         
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)         
           
        self.btn1.clicked.connect(self.make_plot)
        self.btn1.setFixedWidth(80)
        layout = QVBoxLayout()   
        layout.addWidget(self.label1) 
        layout.addWidget(self.countries_ru_list)
        layout.addWidget(self.label2) 
        layout.addWidget(self.seasons_list)    
        layout.addWidget(self.label_space)
        layout.addWidget(self.label3) 
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label4)
        layout.addWidget(self.text_field)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label5)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

    def select_country(self):
        self.seasons_list.clear()
        seasons = Seasons(self.countries_ru_list.currentText())
        self.seasons_list.addItems(seasons.get_seasons()) 

    def select_season(self):
        if self.seasons_list.currentText():
            self.teams_ru_list.clear()  
            clubs_ru = Teams(self.countries_ru_list.currentText(),
                            self.seasons_list.currentText())         
            self.teams_ru_list.addItems(clubs_ru.get_teams())
        else:
            pass
   
    def select_team(self):
        if self.countries_ru_list.currentText() and self.seasons_list.currentText():
            country_and_club_eng = switch_names(self.countries_ru_list.currentText(),
                                            self.teams_ru_list.currentText(),
                                                self.seasons_list.currentText())
            country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1] 
            self.country_and_club_eng_statistics = Citizenship_team(country_eng,
                                                                    self.seasons_list.currentText(),
                                                                    club_eng)
            self.text_field.setPlainText(str(self.country_and_club_eng_statistics.make_dict()))
        else:
            pass
    
    def make_plot(self):
        sizes  = self.country_and_club_eng_statistics.date_for_plot()[1]   
        labels = self.country_and_club_eng_statistics.date_for_plot()[0]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels = labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()


class Tab3(QWidget):
    def __init__(self, fileInfo, parent = None):
        super(Tab3, self).__init__(parent)      
        self.l1 = QLabel('Выбор страны')
        self.c1 = QComboBox()
        self.l11 = QLabel('')
        self.c1.addItems(list(names.country_list.keys()))  
        self.l2 = QLabel('Гражданство всех игроков\n выбранного чемпионата\n текущего\последнего сезона в виде:')
        self.l3 = QLabel('(страна, сколько человек)')
        self.ans = QPlainTextEdit()
        self.ans.setReadOnly(True)
        self.c1.currentIndexChanged.connect(self.select_c1)
        layout = QVBoxLayout()
        layout.addWidget(self.l1)                                
        layout.addWidget(self.c1)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2)
        layout.addWidget(self.l3)
        layout.addWidget(self.ans)
        self.setLayout(layout)

    def select_c1(self):
        self._x1 = Citizenship_country(self.c1.currentText())      
        self.ans.setPlainText(str(self._x1))

    
class Tab4(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab4, self).__init__(parent)
        self.label1 = QLabel('Выбор страны')
        self.countries_ru_list = QComboBox()             
        self.label_space = QLabel('')
        self.label2 = QLabel('Выбор сезона')
        self.seasons_list = QComboBox()                            
        self.label3 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()               
        self.label4 = QLabel('Пятеро незаменимых (больше всего игр)') 
        self.btn1 = QPushButton("Get", self)  
        self.label5 = QLabel('Пятеро самых забивных (больше всего голов)') 
        self.btn2 = QPushButton("Get", self)  
        self.label6 = QLabel('Пятеро самых жёстких (карточки)') 
        self.btn3 = QPushButton("Get", self)  
        self.answer_field = QPlainTextEdit()                        
        self.answer_field.setReadOnly(True)       
        self.countries_ru_list.addItems(list(names.country_list.keys()))
        self.countries_ru_list.currentIndexChanged.connect(self.select_country)   
        self.seasons_list.currentIndexChanged.connect(self.select_season)         
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)       
        self.btn1.clicked.connect(self.get_matches)         
        self.btn2.clicked.connect(self.get_goals)
        self.btn3.clicked.connect(self.get_yellow)    
        self.btn1.setFixedWidth(80)
        self.btn2.setFixedWidth(80)
        self.btn3.setFixedWidth(80)
        layout = QVBoxLayout()   
        layout.addWidget(self.label1) 
        layout.addWidget(self.countries_ru_list)
        layout.addWidget(self.label_space) 
        layout.addWidget(self.label2)
        layout.addWidget(self.seasons_list)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label3)
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.label_space) 
        layout.addWidget(self.label4)
        layout.addWidget(self.btn1)
        layout.addWidget(self.label5)
        layout.addWidget(self.btn2)
        layout.addWidget(self.label6)
        layout.addWidget(self.btn3)
        layout.addWidget(self.label_space) 
        layout.addWidget(self.answer_field)
        self.setLayout(layout)
    
    def select_country(self):
        self.seasons_list.clear()
        seasons = Seasons(self.countries_ru_list.currentText())
        self.seasons_list.addItems(seasons.get_seasons())

    def select_season(self):
        if self.seasons_list.currentText():
            self.teams_ru_list.clear()  
            clubs_ru = Teams(self.countries_ru_list.currentText(), self.seasons_list.currentText())
            self.teams_ru_list.addItems(clubs_ru.get_teams())
        else:
            pass
    
    def select_team(self):
        country_and_club_eng = switch_names(self.countries_ru_list.currentText(),
                                            self.teams_ru_list.currentText(),
                                            self.seasons_list.currentText()) 
        country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1]
        self.answer_field.clear()
        if country_eng and club_eng:                                          
            self.club_statistics = Stats_of_club(country_eng, self.seasons_list.currentText(), club_eng)
        else:
            pass

    def get_matches(self):
        self.answer_field.setPlainText(str(self.club_statistics.matches()))     

    def get_goals(self):
        self.answer_field.setPlainText(str(self.club_statistics.goals()))       

    def get_yellow(self):
        self.answer_field.setPlainText(str(self.club_statistics.yellow_red()))   


class Tab5(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab5, self).__init__(parent)
        self.empty_line = QLabel('')
        self.l1 = QLabel('Игрока под каким № ищем?')    
        self.shoose_number = QComboBox()
        self.shoosed_player_number = "" 
        self.l2 = QLabel('Выбор страны')
        self.countries_ru_list = QComboBox()      
        self.l3 = QLabel('Выбор сезона')
        self.seasons_list = QComboBox()      
        self.l4 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()            
        self.btn = QPushButton("Go!", self)                     
        self.text_field = QPlainTextEdit()          
        self.text_field.setReadOnly(True)
        self.shoose_number.addItems([str(i) for i in range(1,100,1)])
        self.shoose_number.activated[str].connect(self.set_number)     
        self.countries_ru_list.addItems(list(names.country_list.keys()))         
        self.countries_ru_list.currentIndexChanged.connect(self.select_country)  
        self.seasons_list.currentIndexChanged.connect(self.select_season)
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)        
        self.btn.clicked.connect(self.get_player_func)
        self.btn.setFixedWidth(80)
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.shoose_number)
        layout.addWidget(self.empty_line)
        layout.addWidget(self.l2)
        layout.addWidget(self.countries_ru_list)
        layout.addWidget(self.empty_line)
        layout.addWidget(self.l3)
        layout.addWidget(self.seasons_list)
        layout.addWidget(self.empty_line)
        layout.addWidget(self.l4)
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.empty_line)
        layout.addWidget(self.btn)
        layout.addWidget(self.empty_line)
        layout.addWidget(self.text_field)
        self.setLayout(layout)

    def set_number(self, text):
        self.l1.setText('')
        self.l1.setText('Ищем игрока под № {}'.format(text))
        self.shoosed_player_number = text

    def select_country(self):
        self.seasons_list.clear()
        seasons = Seasons(self.countries_ru_list.currentText())
        self.seasons_list.addItems(seasons.get_seasons())

    def select_season(self):
        if self.seasons_list.currentText():
            self.teams_ru_list.clear()  
            clubs_ru = Teams(self.countries_ru_list.currentText(), self.seasons_list.currentText())
            self.teams_ru_list.addItems(clubs_ru.get_teams())
        else:
            pass
        
    def select_team(self):
        country_and_club_eng = switch_names(self.countries_ru_list.currentText(),
                                            self.teams_ru_list.currentText(),
                                            self.seasons_list.currentText())
        country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1]
        self.text_field.clear()                            
        if country_eng and club_eng:
            self.get_player = get_number_player(country_eng, self.seasons_list.currentText(),
                                                club_eng, self.shoosed_player_number)
        else:
            pass
    
    def get_player_func(self):
        self.text_field.setPlainText(str(self.get_player))      

       
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."
    maindialog = MainDialog(fileName)
    sys.exit(maindialog.exec_())

    
