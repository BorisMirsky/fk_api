# coding: utf8


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import matplotlib.pyplot as plt
from matplotlib import rc

#import html5lib
import requests
from number9 import Get_9, Get_9s
import names
from Teams import Teams                                 # примет страну выдаст клубы
from Switch_names import Country_team                   # переключит названия клубов с русского на английский
from Citizenship_team import Citizenship_team           # примет страну и клуб, выдаст гражданства клуба
from Citizenship_country import Citizenship_country     # примет страну выдаст гражданства страны
from pandas1 import Do_pandas                           # примет страну и клуб, выдаст игроков с наибольшим количеством игр, голов,
                                                        #         жёлтых/красных карточек
font = {'family': 'DejaVu Sans','weight': 'normal'}     # шрифт для Ubuntu 
rc('font', **font)                                      #  то же самое


class MenuBar(QWidget):         # Верхняя панель меню, не иcпользуется
    def __init__(self):
        super(MenuBar, self).__init__()
        self.setWindowTitle('message box')
        self.createActions()
        self.createMenus()
    
    def new(self):                                           
        pass
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
               "Open File", QtCore.QDir.currentPath())              	
    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                "Save File As", QtCore.QDir.currentPath())
    def about(self):
        QtGui.QMessageBox.about(self, "About Menu",             
        "The <b>Menu</b> example shows how to create menu-bar menus "
        "and context menus.")      	
    def aboutQt(self):
        QtGui.QMessageBox.aboutQt(self)
    def createActions(self):
        self.newAct = QAction("New", self, triggered=self.new)  
        self.openAct = QAction("Open", self, triggered=self.open)
        self.saveAsAct = QAction("SaveAs", self, triggered=self.saveAs)
        self.aboutAct = QAction("About", self, triggered=self.about)
        self.aboutQtAct = QAction("About Qt", self, triggered=self.aboutQt)                          
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")    
        self.fileMenu.addAction(self.newAct)               
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.helpMenu = self.menuBar().addMenu("Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)       


class MainDialog(QDialog):        # Основной элемент для вкладок (Tabs)
    def __init__(self, fileName, parent=None):
        super(MainDialog, self).__init__(parent)  
        fileInfo = QFileInfo(fileName)          
        tabWidget = QTabWidget()  
        tabWidget.addTab(Tab1(fileInfo), "Tab1")
        tabWidget.addTab(Tab2(fileInfo), "Tab2")
        tabWidget.addTab(Tab3(fileInfo), "Tab3")
        tabWidget.addTab(Tab4(fileInfo), "Tab4")
        tabWidget.addTab(Tab5(fileInfo), "Tab5")
        tabWidget.addTab(Tab6(fileInfo), "Tab6")
        mainLayout = QVBoxLayout()
        #mainLayout.addWidget(MenuBar())
        mainLayout.addWidget(tabWidget)
        mainLayout.addStretch(0)
        self.setLayout(mainLayout)
        self.setWindowTitle("API for football.kulichki")
        self.setWindowIcon(QIcon('tshirt_icon.png'))     
        self.resize(300, 550)                               
        self.move(150, 150)
        self.sshFile="darkorange.stylesheet"            # Внешний файл с таблицей стилей 
        with open(self.sshFile,"r") as fh:              #    взят здесь: http://www.yasinuludag.com/darkorange.stylesheet
            self.setStyleSheet(fh.read())


class Tab1(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab1, self).__init__(parent)
        l1 = QLabel('Сайт "Футбол на Куличках" \nпопулярен'
                          ' как удобный и достоверный\n источник статистических данных о футболе.'
                           '\n\nЭта программа '
                          'обрабатывает\nнекоторые параметры команд и игроков.\n'
                          'Используются внешние парсеры, matplotlib, pandas.\n'
                          'Все данные создаются динамически.')
        layout = QVBoxLayout()
        layout.addWidget(l1)
        self.setLayout(layout)

      
class Tab2(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab2, self).__init__(parent)
        self.l1 = QLabel('Выбор страны')
        self.c = QComboBox()               # 1й выпадающий список "Страны"
        self.l11 = QLabel('')
        self.l2 = QLabel('Выбор команды')
        self.t = QComboBox()               # 2й выпадающий список "Команды"
        self.l22 = QLabel('')
        self.l3 = QLabel('Гражданство игроков команды')          
        self.ans1 = QPlainTextEdit()                         # текстовое поле
        self.ans1.setReadOnly(True)
        self.l33 = QLabel('')
        self.l4 = QLabel('Получить график') 
        self.btn1 = QPushButton("Get plot", self)            # кнопка
        self.c.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c.currentIndexChanged.connect(self.select_c)          # при выборе из c запускается select_c
        self.t.currentIndexChanged.connect(self.select_t)          # при выборе из t запускается select_t
        self.btn1.clicked.connect(self.make_plot)                  # появляется график при нажатии на кнопку
        self.btn1.setFixedWidth(80)
        layout = QVBoxLayout()   
        layout.addWidget(self.l1) 
        layout.addWidget(self.c)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2) 
        layout.addWidget(self.t)
        layout.addWidget(self.l22)
        layout.addWidget(self.l3)
        layout.addWidget(self.ans1)
        layout.addWidget(self.l33)
        layout.addWidget(self.l4)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

    # запускается при выборе из 1-го выпадающего списка "c"
    # select_c
    def select_c(self):                       
        x = Teams(self.c.currentText())         # Teams.Teams примет страну по русски, выдаст список клубы по русски
        x1 = x.make_dict()                      # выдаст в правильном формате
        self.t.clear()                          # очистить список t
        self.t.addItems(x1)                     # список клубов передан в t
        self.ans1.clear()

    # запускается при выборе из 2-го выпадающего списка "t"
    def select_t(self):                   
        x = Country_team(self.c.currentText(), self.t.currentText()) # Примет страну и клуб по русски, "переключит" их на английский
        x1 = x.switch_names()[0]                                     # страна по английски
        x2 = x.switch_names()[1]                                     # клуб по английски
        self.x3 = Citizenship_team(x1, x2)                           # передача страны и клуба в парсинг для подсчёта гражданства
        self.ans1.setPlainText(str(self.x3.make_dict()))             # передать результат парсинга в текстовое поле

    def make_plot(self):
        sizes  = self.x3.date_for_plot()[1]   
        labels = self.x3.date_for_plot()[0]   
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
        self.c1.addItems(names.country_list_2)
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
        self._x1 = Citizenship_country(self.c1.currentText())      # 
        self.ans.setPlainText(str(self._x1))

    
class Tab4(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab4, self).__init__(parent)
        self.l1 = QLabel('Выбор страны')
        self.c = QComboBox()               # 1й выпадающий список "Страны"
        self.l11 = QLabel('')
        self.l2 = QLabel('Выбор команды')
        self.t = QComboBox()               # 2й выпадающий список "Команды"
        self.l22 = QLabel('')
        self.l3 = QLabel('Пятеро незаменимых (больше всего игр)') 
        self.btn1 = QPushButton("Get", self)  # кнопка 
        self.l4 = QLabel('Пятеро самых забивных (больше всего голов)') 
        self.btn2 = QPushButton("Get", self)  # кнопка
        self.l5 = QLabel('Пятеро самых жёстких (карточки)') 
        self.btn3 = QPushButton("Get", self)  # кнопка
        self.l33 = QLabel('')
        self.ans = QPlainTextEdit()                          # текстовое поле
        self.ans.setReadOnly(True)
        
        self.c.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c.currentIndexChanged.connect(self.select_c)          # при выборе из c запускается select_c
        self.t.currentIndexChanged.connect(self.select_t)          # при выборе из t запускается select_t

        self.btn1.clicked.connect(self.get_matches)                 # coding: utf8)
        self.btn2.clicked.connect(self.get_goals)
        self.btn3.clicked.connect(self.get_yellow)
        
        self.btn1.setFixedWidth(80)
        self.btn2.setFixedWidth(80)
        self.btn3.setFixedWidth(80)
        layout = QVBoxLayout()   
        layout.addWidget(self.l1) 
        layout.addWidget(self.c)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2) 
        layout.addWidget(self.t)
        layout.addWidget(self.l22)
        layout.addWidget(self.l3)
        layout.addWidget(self.btn1)
        layout.addWidget(self.l4)
        layout.addWidget(self.btn2)
        layout.addWidget(self.l5)
        layout.addWidget(self.btn3)
        layout.addWidget(self.l33)
        layout.addWidget(self.ans)
        self.setLayout(layout)
    
    # запускается при выборе из 1-го выпадающего списка "c"
    def select_c(self):
        x = Teams(self.c.currentText())         # Teams.Teams: страна по русски --> клубы по русски
        #x1 = x.make_dict()                      # выдаст в правильном формате
        self.t.clear()                          # очистить QComboBox t
        self.t.addItems(["", "1", "2", "3"])                    # список клубов передан в t
        #self.t.addItems(x)
       
    # запускается при выборе из 2-го выпадающего списка "t"
    def select_t(self):
        x = Country_team(self.c.currentText(), self.t.currentText()) # Страна и клуб по русски--> по английски
        x1 = x.switch_names()[0]            # страна по английски
        x2 = x.switch_names()[1]            # клуб по английски
        self.ans.clear()
        self.x3 = Do_pandas(x1, x2)          # передача страны и клуба 

    def get_matches(self):
        #print(str(self.x3.matches()))
        self.ans.setPlainText(str(self.x3.matches()))      # передать в текстовое поле

    def get_goals(self):
        #print(str(self.x3.goals()))
        self.ans.setPlainText(str(self.x3.goals()))        # передать в текстовое поле

    def get_yellow(self):
        #print(str(self.x3.yellow_red()))
        self.ans.setPlainText(str(self.x3.yellow_red()))   # передать в текстовое поле


class Tab5(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab5, self).__init__(parent)
        self.l1 = QLabel('Всегда нравились игроки под №9')
        self.l11 = QLabel('')
        self.l2 = QLabel('Выбор страны')
        self.c1 = QComboBox()                         # 1й выпадающий список "Страны"
        self.l3 = QLabel('Выбор команды')
        self.t = QComboBox()                         # 2й выпадающий список "Команды"
        self.btn1 = QPushButton("Get 9", self)       # кнопка выбора №1
        self.l33 = QLabel('')                        # пустая строка
        self.l4 = QLabel('Выбор страны')
        self.c2 = QComboBox()                        # 3й выпадающий список "Страны"
        self.btn2 = QPushButton("Get 9s", self)      # кнопка выбора №2
                
        self.l5 = QLabel('') 
        self.ans = QPlainTextEdit()                          # текстовое поле
        self.ans.setReadOnly(True)
        
        self.c1.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c1.currentIndexChanged.connect(self.select_c1)         # при выборе из c1 запускается select_c1
        self.t.currentIndexChanged.connect(self.select_t)           # при выборе из t запускается select_t

        self.c2.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c2.currentIndexChanged.connect(self.select_c2)         # при выборе из c1 запускается select_c1

        self.btn1.clicked.connect(self.get_extract_9)
        self.btn2.clicked.connect(self.get_extract_9s)

        self.btn1.setFixedWidth(80)
        self.btn2.setFixedWidth(80)
        layout = QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2)
        layout.addWidget(self.c1)
        layout.addWidget(self.l3) 
        layout.addWidget(self.t)
        layout.addWidget(self.btn1)
        layout.addWidget(self.l33)
        layout.addWidget(self.l4)
        layout.addWidget(self.c2)
        layout.addWidget(self.btn2)
        layout.addWidget(self.l5)
        layout.addWidget(self.ans)
        self.setLayout(layout)

    # запускается при выборе из 1-го выпадающего списка "c1"
    def select_c1(self):                       
        x = Teams(self.c1.currentText())         # Teams.Teams: страна по русски --> клубы по русски
        x1 = x.make_dict()                      # выдаст в правильном формате
        self.t.clear()                          # очистить список t
        self.t.addItems(x1)                     # список клубов передан в t
       
    # запускается при выборе из 2-го выпадающего списка "t"
    def select_t(self):
        x = Country_team(self.c1.currentText(), self.t.currentText()) # Страна и клуб по русски--> по английски
        x1 = x.switch_names()[0]                              # страна по английски
        x2 = x.switch_names()[1]                              # клуб по английски
        self.ans.clear()
        self.x3 = Get_9(x1, x2)                               # передача страны и клуба

    def get_extract_9(self):
        self.ans.setPlainText(str(self.x3.extract_9()))                   #.extract_9()))      # передать в текстовое поле

    # запускается при выборе из 2-го выпадающего списка "c2"
    def select_c2(self):                       
        x = Teams(self.c2.currentText())         # Teams.Teams: страна по русски --> клубы по русски
        x1 = x.make_dict()                      # выдаст в правильном формате
        self.x2 = Get_9s(x1)

    def get_extract_9s(self):
        self.ans.setPlainText(str(self.x2.extract_9s()))      # передать в текстовое поле
             


class Tab6(QWidget):                                       # Новости + Аналитика (возможно)
    def __init__(self, fileInfo, parent=None):
        super(Tab6, self).__init__(parent)
        self.l1 = QLabel('Выбор страны')
        self.c = QComboBox()                                 # 1й выпадающий список "Страны"
        self.l11 = QLabel('')
        self.l2 = QLabel('Выбор команды')
        self.t = QComboBox()                                 # 2й выпадающий список "Команды"
        self.l22 = QLabel('')
        self.l3 = QLabel('Все "девятки" чемпионата') 
        self.ans = QPlainTextEdit()                          # текстовое поле
        self.ans.setReadOnly(True)
        self.c.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
     #   self.c.currentIndexChanged.connect(self.select_c)          # при выборе из c запускается select_c
     #   self.t.currentIndexChanged.connect(self.select_t)          # при выборе из t запускается select_t
        layout = QVBoxLayout()   
        layout.addWidget(self.l1) 
        layout.addWidget(self.c)
        layout.addWidget(self.l11)
        layout.addWidget(self.l2) 
        layout.addWidget(self.t)
        layout.addWidget(self.l22)
        layout.addWidget(self.l3)
        layout.addWidget(self.ans)
        self.setLayout(layout)


             
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."
    maindialog = MainDialog(fileName)
    sys.exit(maindialog.exec_())

    
