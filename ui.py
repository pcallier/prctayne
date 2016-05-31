#!/usr/bin/env python
"""
ui.py
Patrick Callier
May 2016

Simple UI for playing sequences prctayne proposes
and thumbing them up or down?
"""

from PyQt5.QtWidgets import QApplication, QWidget

def show_gui():
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250,10)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())
