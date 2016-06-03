#!/usr/bin/env python
"""
ui.py
Patrick Callier
May 2016

Simple UI for playing sequences prctayne proposes
and thumbing them up or down?
"""

import sys 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Form(QWidget): 
    def __init__(self , parent=None):
        super(Form, self).__init__(parent)
        nameLabel = QLabel("Name")
        self.nameLine = QLineEdit()
        self.submitButton = QPushButton(r"&Submit")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submitContact)

        mainLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")

        self.play_shortcut = QShortcut(QKeySequence("Tab"), self)
        self.play_shortcut.activated.connect(self.on_play)

    @pyqtSlot()
    def on_play(self):
        QMessageBox.information(self, "Message", " Play!")

    def submitContact(self):
        name = self.nameLine.text()

        if name == "":
            QMessageBox.information(self, "Empty Field", "Please enter a name and address.")
            return
        else:
             QMessageBox.information(self, "Success!", "Hello {}!".format(name))


def show_gui():
    app = QApplication(sys.argv)
    screen = Form()
    screen.show()

    sys.exit(app.exec_())

if __name__=="__main__":
    show_gui()
