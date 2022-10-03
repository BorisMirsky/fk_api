# coding: utf8

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import time

# the same project
from number9 import func_get9, func_get9s
import names
from Teams import Teams                                 # примет страну выдаст клубы
from Switch_names import switch_names #Country_team                   # переключит названия клубов с русского на английский
from Citizenship_team import Citizenship_team           # примет страну и клуб, выдаст гражданства клуба
from Citizenship_country import Citizenship_country     # примет страну выдаст гражданства страны
from pandas_stats import Stats_of_club                           # примет страну и клуб, выдаст игроков с наибольшим количеством игр, голов,
                                                        #         жёлтых/красных карточек
                 
font = {'family': 'DejaVu Sans','weight': 'normal'}     # шрифт для Ubuntu 
rc('font', **font)                                      # то же самое



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
        self.setWindowIcon(QIcon('tshirt_icon.png'))     
        self.resize(300, 550)                               
        self.move(150, 150)
        self.sshFile="darkorange.stylesheet"   # Внешний файл с таблицей стилей взят здесь:
        with open(self.sshFile,"r") as fh:     # http://www.yasinuludag.com/darkorange.stylesheet
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
        self.countries_ru_list = QComboBox()               # 1й выпадающий список "Страны"
        self.label_space = QLabel('')
        self.label2 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()               # 2й выпадающий список "Команды"
        self.label3 = QLabel('Гражданство игроков команды')          
        self.text_field = QPlainTextEdit()                         # текстовое поле
        self.text_field.setReadOnly(True)
        self.label4 = QLabel('Получить график') 
        self.btn1 = QPushButton("Get plot", self)   
        self.countries_ru_list.addItems(list(names.country_list.keys()))          # список стран по русски вставили в 1й выпадающий список
        self.countries_ru_list.currentIndexChanged.connect(self.select_country)   # при выборе из c запускается select_country
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)          # при выборе из t запускается select_team
        #  Вот тут надо связывать Синглтон и график
        self.btn1.clicked.connect(self.make_plot)                  # появляется график при нажатии на кнопку
        self.btn1.setFixedWidth(80)
        layout = QVBoxLayout()   
        layout.addWidget(self.label1) 
        layout.addWidget(self.countries_ru_list)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label2) 
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label3)
        layout.addWidget(self.text_field)
        layout.addWidget(self.label_space)
        layout.addWidget(self.label4)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

    # запускается при выборе из 1-го выпадающего списка "c"
    def select_country(self):
        clubs_ru = Teams(self.countries_ru_list.currentText())  # Teams.Teams примет страну по русски, выдаст список 'клубы по русски'
        clubs_ru_formatted = clubs_ru.make_dict()               # выдаст в правильном формате
        self.teams_ru_list.clear()                              # очистить список t
        self.teams_ru_list.addItems(clubs_ru_formatted)         # список клубов передан в t
        self.text_field.clear()

    # запускается при выборе из 2-го выпадающего списка "t"
    def select_team(self):                   
        country_and_club_eng = switch_names(self.countries_ru_list.currentText(),
                                            self.teams_ru_list.currentText()) # Примет страну и клуб по русски, "переключит" их на английский
        country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1] 
        self.country_and_club_eng_statistics = Citizenship_team(country_eng, club_eng)                  # передача страны и клуба в парсинг для подсчёта гражданства
        self.text_field.setPlainText(str(self.country_and_club_eng_statistics.make_dict()))             # передать результат парсинга в текстовое поле
    
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
        self.c1.addItems(list(names.country_list.keys()))  #names.country_list_2)
        self.l2 = QLabel('Гражданство всех игроков чемпионата в виде:')
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
        self.label2 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()               
        self.label3 = QLabel('Пятеро незаменимых (больше всего игр)') 
        self.btn1 = QPushButton("Get", self)  
        self.label4 = QLabel('Пятеро самых забивных (больше всего голов)') 
        self.btn2 = QPushButton("Get", self)  
        self.label5 = QLabel('Пятеро самых жёстких (карточки)') 
        self.btn3 = QPushButton("Get", self)  
        self.ans = QPlainTextEdit()                        
        self.ans.setReadOnly(True)
        
        self.countries_ru_list.addItems(list(names.country_list.keys()))          # список стран по русски вставили в 1й ComboBox
        self.countries_ru_list.currentIndexChanged.connect(self.select_country)   # при выборе из c запускается select_country
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)          # при выборе из t запускается select_team

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
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.label_space) 
        layout.addWidget(self.label3)
        layout.addWidget(self.btn1)
        layout.addWidget(self.label4)
        layout.addWidget(self.btn2)
        layout.addWidget(self.label5)
        layout.addWidget(self.btn3)
        layout.addWidget(self.label_space) 
        layout.addWidget(self.ans)
        self.setLayout(layout)
    
    # запускается при выборе из 1-го выпадающего списка "c"
    def select_country(self):
        time.sleep(1)
        clubs_ru = Teams(self.countries_ru_list.currentText())         # Teams.Teams: страна по русски --> клубы по русски
        clubs_ru_formatted = clubs_ru.make_dict()                      # выдача в правильном формате
        self.teams_ru_list.clear()                                     # очистить QComboBox t
        self.teams_ru_list.addItems(clubs_ru_formatted)                # добавляет в teams
        self.ans.clear()
       
    # запускается при выборе из 2-го выпадающего списка "t"
    def select_team(self):
        country_and_club_eng = switch_names(self.countries_ru_list.currentText(),
                                            self.teams_ru_list.currentText()) # Страна и клуб по русски--> по английски
        country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1]
        self.ans.clear()
        time.sleep(1)
        if country_eng and club_eng:                                          # Error processing
            self.club_statistics = Stats_of_club(country_eng, club_eng)
        else:
            pass

    def get_matches(self):
        self.ans.setPlainText(str(self.club_statistics.matches()))      # передать в текстовое поле

    def get_goals(self):
        self.ans.setPlainText(str(self.club_statistics.goals()))        # передать в текстовое поле

    def get_yellow(self):
        self.ans.setPlainText(str(self.club_statistics.yellow_red()))   # передать в текстовое поле


class Tab5(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab5, self).__init__(parent)
        self.l1 = QLabel('Всегда нравились игроки под №9')
        self.l11 = QLabel('')
        self.l2 = QLabel('Выбор страны')
        self.countries_ru_list_1 = QComboBox()                         # 1й выпадающий список "Страны"
        self.l3 = QLabel('Выбор команды')
        self.teams_ru_list = QComboBox()                         # 2й выпадающий список "Команды"
        self.btn1 = QPushButton("Get 9", self)       # кнопка выбора №1
        self.l33 = QLabel('')                        # пустая строка
        self.l4 = QLabel('Выбор страны')
        self.countries_ru_list_2 = QComboBox()                        # 3й выпадающий список "Страны"
        self.btn2 = QPushButton("Get 9s", self)      # кнопка выбора №2
                
        self.l5 = QLabel('') 
        self.text_field = QPlainTextEdit()                          # текстовое поле
        self.text_field.setReadOnly(True)
        
        self.countries_ru_list_1.addItems(list(names.country_list.keys()))           # список стран по русски вставили в 1й выпадающий список
        self.countries_ru_list_1.currentIndexChanged.connect(self.select_country_1)         # при выборе из c1 запускается select_c1
        self.teams_ru_list.currentIndexChanged.connect(self.select_team)           # при выборе из t запускается select_t

        self.countries_ru_list_2.addItems(list(names.country_list.keys())) # список стран по русски вставили в 1й выпадающий список
        self.countries_ru_list_2.currentIndexChanged.connect(self.select_country_2)         # при выборе из c2 запускается select_c2

        self.btn1.clicked.connect(self.get_extract_9)
        self.btn2.clicked.connect(self.get_extract_9s)

        self.btn1.setFixedWidth(80)
        self.btn2.setFixedWidth(80)
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2)
        layout.addWidget(self.countries_ru_list_1)
        layout.addWidget(self.l3) 
        layout.addWidget(self.teams_ru_list)
        layout.addWidget(self.btn1)
        layout.addWidget(self.l33)
        layout.addWidget(self.l4)
        layout.addWidget(self.countries_ru_list_2)
        layout.addWidget(self.btn2)
        layout.addWidget(self.l5)
        layout.addWidget(self.text_field)
        self.setLayout(layout)

    # запускается при выборе из 1-го выпадающего списка "c1"
    def select_country_1(self):
        clubs_ru = Teams(self.countries_ru_list_1.currentText())        # Teams.Teams: страна по русски --> клубы по русски
        clubs_ru_formatted = clubs_ru.make_dict()                       # выдаст в правильном формате
        self.teams_ru_list.clear()
        self.teams_ru_list.addItems(clubs_ru_formatted)                 # список клубов передан в t
        self.text_field.clear()

    # запускается при выборе из 2-го выпадающего списка "t"
    def select_team(self):
        country_and_club_eng = switch_names(self.countries_ru_list_1.currentText(),
                                       self.teams_ru_list.currentText()) # Страна и клуб по русски--> по английски
        country_eng, club_eng = country_and_club_eng[0], country_and_club_eng[1]
        self.text_field.clear()                            
        if country_eng and club_eng:                                          # Error processing
            self.get9_instance = func_get9(country_eng, club_eng)             # передача страны и клуба
        else:
            pass
    
    def get_extract_9(self):
        self.text_field.setPlainText(str(self.get9_instance))       # передать в текстовое поле

    # запускается при выборе из 2-го выпадающего списка "c2"
    def select_country_2(self):
        self.text_field.clear()
        country_lat = names.country_list[self.countries_ru_list_2.currentText()]
        self.get9s_instance = func_get9s(country_lat)           

    def get_extract_9s(self):
        self.text_field.setPlainText(str(self.get9s_instance))      # передать в текстовое поле
             


             
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."
    maindialog = MainDialog(fileName)
    sys.exit(maindialog.exec_())

    
