# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from time import sleep
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import datetime

# Write time and date of new Session
current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
date = current_time.day
hour = current_time.hour
minute = current_time.minute
second = current_time.second
date_str = ('\n\n' + '                                        New Session - ' + str(date) + ' / ' + str(month) + ' / ' + str(year) + '\n' +
            '                                          On Time - ' + str(hour) + ' : ' + str(minute) + ' : ' + str(second) + '\n')
file = open('Chat Record.txt', 'a')
file.write(str(date_str))
file.close()


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, pn_message):
        print('incoming_message', pn_message.message)
        ui.new_messages.append(pn_message.message)
        while ui.new_messages:
            if len(ui.new_messages) > 0:
                msg = ui.new_messages.pop(0)
                msg = ui.format_message(msg)
                ui.text_area.appendPlainText(msg)

                current_time = datetime.datetime.now()
                hour = current_time.hour
                minute = current_time.minute
                second = current_time.second

                file = open('Chat Record.txt', 'a')
                file.write('\n'+str(hour) + ' : ' + str(minute) +
                           ' : ' + str(second) + ' - ' + msg)
                file.close()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.text_area = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_area.setGeometry(QtCore.QRect(10, 159, 780, 321))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_area.setFont(font)
        self.text_area.setTabChangesFocus(False)
        self.text_area.setReadOnly(True)
        self.text_area.setBackgroundVisible(False)
        self.text_area.setCenterOnScroll(False)
        self.text_area.setObjectName("text_area")
        self.message_input = QtWidgets.QLineEdit(self.centralwidget)
        self.message_input.setGeometry(QtCore.QRect(10, 490, 780, 50))
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(10, 540, 780, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.message_input.setFont(font)
        self.message_input.setText("")
        self.message_input.setObjectName("message_input")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.channel = 'chat-channel'
        pnconfig = PNConfiguration()

        pnconfig.publish_key = 'pub-c-4c03cf9a-687e-46e7-b1ba-ab62e84bba78'
        pnconfig.subscribe_key = 'sub-c-22fb1c63-ab41-4e2f-a9a2-5e20d62ce2c3'

        self.pubnub = PubNub(pnconfig)
        self.retranslateUi(MainWindow)
        self.new_messages = []
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Project"))
        self.pubnub.add_listener(MySubscribeCallback())
        self.pubnub.subscribe().channels(self.channel).execute()
        # self.message_input.returnPressed.connect(self.send_message)

    def format_message(self, message_body):
        return message_body.get('name') + ": " + message_body.get('message')

    def pubnub_publish(self, data):
        self.pubnub.publish().channel(self.channel).message(data).sync()

    def display_new_messages(self):
        while self.new_messages:
            if len(self.new_messages) > 0:
                msg = self.new_messages.pop(0)
                msg = self.format_message(msg)
        #        self.text_area.appendPlainText(msg)

    def send_message(self):
        # print(self.message_input.text())
        self.pubnub_publish(
            {"name": self.name.text(), "message": self.message_input.text()})
        self.message_input.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    ui.message_input.returnPressed.connect(ui.send_message)
    timer = QTimer()
    timer.timeout.connect(ui.display_new_messages)
    timer.start(1000)

    sys.exit(app.exec())