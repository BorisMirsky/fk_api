# coding: utf8

from PyQt4 import QtGui, QtCore
import sys
import matplotlib.pyplot as plt
from matplotlib import rc

import names
from Teams import Teams                                 # примет страну выдаст клубы
from Switch_names import Country_team                   # переключит названия клубов с русского на английский
from Citizenship_team import Citizenship_team           # примет страну и клуб, выдаст гражданства клуба
from Citizenship_country import Citizenship_country     # примет страну выдаст гражданства страны
from pandas1 import Do_pandas                           # примет страну и клуб, выдаст игроков с наибольшим количеством игр, голов,
                                                        #         жёлтых/красных карточек
font = {'family': 'DejaVu Sans','weight': 'normal'}     # шрифт для Ubuntu 
rc('font', **font)                                      # -------//-------


class MenuBar(QtGui.QMainWindow):                      # Панель меню, не иcпользуется, элемент декора
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
        self.newAct = QtGui.QAction("New", self, triggered=self.new)  
        self.openAct = QtGui.QAction("Open", self, triggered=self.open)
        self.saveAsAct = QtGui.QAction("SaveAs", self, triggered=self.saveAs)
        self.aboutAct = QtGui.QAction("About", self, triggered=self.about)
        self.aboutQtAct = QtGui.QAction("About Qt", self, triggered=self.aboutQt)                          
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")    
        self.fileMenu.addAction(self.newAct)               
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.helpMenu = self.menuBar().addMenu("Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)       


class MainDialog(QtGui.QDialog):                      # Основной элемент для вкладок (Tabs)
    def __init__(self, fileName, parent=None):
        super(MainDialog, self).__init__(parent)
        fileInfo = QtCore.QFileInfo(fileName)         # 
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(Tab1(fileInfo), "Tab1")
        tabWidget.addTab(Tab2(fileInfo), "Tab2")
        tabWidget.addTab(Tab3(fileInfo), "Tab3")
        tabWidget.addTab(Tab4(fileInfo), "Tab4")
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(MenuBar())
        mainLayout.addWidget(tabWidget)
        mainLayout.addStretch(0)
        self.setLayout(mainLayout)
        self.setWindowTitle("API for football.kulichki")
        self.setWindowIcon(QtGui.QIcon('tshirt_icon.png'))     
        self.resize(300, 400)                               
        self.move(150, 150)
        self.sshFile="darkorange.stylesheet"    # Stylesheet
        with open(self.sshFile,"r") as fh:      #      from http://www.yasinuludag.com/darkorange.stylesheet
            self.setStyleSheet(fh.read())


class Tab1(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab1, self).__init__(parent)
        l1 = QtGui.QLabel('Сайт "Футбол на Куличках" \nпопулярен'
                          ' как удобный и достоверный\n источник статистических данных о футболе.'
                           '\n\nЭта программа '
                          'обрабатывает\nнекоторые параметры команд и игроков.\n'
                          'Используются внешние парсеры, matplotlib, pandas.\n'
                          'Все данные создаются динамически.')
#        l1.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')
        layout = QtGui.QVBoxLayout()
        layout.addWidget(l1)
        self.setLayout(layout)

      
class Tab2(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab2, self).__init__(parent)
        self.l1 = QtGui.QLabel('Выбор страны')
        self.c = QtGui.QComboBox()               # 1й выпадающий список "Страны"
        self.l11 = QtGui.QLabel('')
        self.l2 = QtGui.QLabel('Выбор команды')
        self.t = QtGui.QComboBox()               # 2й выпадающий список "Команды"
        self.l22 = QtGui.QLabel('')
        self.l3 = QtGui.QLabel('Гражданство игроков команды')          
        self.ans1 = QtGui.QPlainTextEdit()                         # текстовое поле
        self.l33 = QtGui.QLabel('')
        self.l4 = QtGui.QLabel('Получить график') 
        self.btn1 = QtGui.QPushButton("Get plot", self)  # кнопка
        self.c.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c.currentIndexChanged.connect(self.select_c)          # при выборе из c запускается select_c
        self.t.currentIndexChanged.connect(self.select_t)          # при выборе из t запускается select_t
        self.btn1.clicked.connect(self.make_plot)                  # появляется график при нажатии на кнопку
        self.btn1.setFixedWidth(80)
        layout = QtGui.QVBoxLayout()   
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
                     
class Tab3(QtGui.QWidget):
    def __init__(self, fileInfo, parent = None):
        super(Tab3, self).__init__(parent)
        
        self.l1 = QtGui.QLabel('Выбор страны')
        self.c1 = QtGui.QComboBox()
        self.l11 = QtGui.QLabel('')
        self.c1.addItems(names.country_list_2)
        self.l2 = QtGui.QLabel('Гражданство всех игроков чемпионата в виде:')
        self.l3 = QtGui.QLabel('(страна, сколько человек)')
        self.ans = QtGui.QPlainTextEdit()
        self.c1.currentIndexChanged.connect(self.select_c1)
        layout = QtGui.QVBoxLayout()
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

    
class Tab4(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(Tab4, self).__init__(parent)
        self.l1 = QtGui.QLabel('Выбор страны')
        self.c = QtGui.QComboBox()               # 1й выпадающий список "Страны"
        self.l11 = QtGui.QLabel('')
        self.l2 = QtGui.QLabel('Выбор команды')
        self.t = QtGui.QComboBox()               # 2й выпадающий список "Команды"
        self.l22 = QtGui.QLabel('')
        self.l3 = QtGui.QLabel('Пятеро незаменимых (больше всего игр)') 
        self.btn1 = QtGui.QPushButton("Get", self)  # кнопка 
        self.l4 = QtGui.QLabel('Пятеро самых забивных (больше всего голов)') 
        self.btn2 = QtGui.QPushButton("Get", self)  # кнопка
        self.l5 = QtGui.QLabel('Пятеро самых жёстких (карточки)') 
        self.btn3 = QtGui.QPushButton("Get", self)  # кнопка
        self.l33 = QtGui.QLabel('')
        self.ans = QtGui.QPlainTextEdit()                         # текстовое поле
        self.c.addItems(names.country_list_2)                      # список стран по русски вставили в 1й выпадающий список
        self.c.currentIndexChanged.connect(self.select_c)          # при выборе из c запускается select_c
        self.t.currentIndexChanged.connect(self.select_t)          # при выборе из t запускается select_t
        self.btn1.clicked.connect(self.get_matches)
        self.btn2.clicked.connect(self.get_goals)
        self.btn3.clicked.connect(self.get_yellow)
        self.btn1.setFixedWidth(80)
        self.btn2.setFixedWidth(80)
        self.btn3.setFixedWidth(80)
        layout = QtGui.QVBoxLayout()   
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
        x1 = x.make_dict()                      # выдаст в правильном формате
        self.t.clear()                          # очистить список t
        self.t.addItems(x1)                     # список клубов передан в t
       
    # запускается при выборе из 2-го выпадающего списка "t"
    def select_t(self):
        x = Country_team(self.c.currentText(), self.t.currentText()) # Страна и клуб по русски--> по английски
        x1 = x.switch_names()[0]            # страна по английски
        x2 = x.switch_names()[1]            # клуб по английски
        self.ans.clear()
        self.x3 = Do_pandas(x1, x2)          # передача страны и клуба 

    def get_matches(self):
        self.ans.setPlainText(str(self.x3.matches()))   # передать в текстовое поле

    def get_goals(self):
        self.ans.setPlainText(str(self.x3.goals()))   # передать в текстовое поле

    def get_yellow(self):
        self.ans.setPlainText(str(self.x3.yellow_red()))   # передать в текстовое поле

             
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."
    maindialog = MainDialog(fileName)
    sys.exit(maindialog.exec_())
    
# in manual:  433 - connect, 520 - ComboBox, 497 - PlainTextEdit
