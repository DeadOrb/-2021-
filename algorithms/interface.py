#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import lossless.arithmetic_encoding as arithm


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        lbl = QLabel(self)
        lbl.setText("Open file for en/de-coding")
        lbl.move(30, 30)

        self.qle_file = QLineEdit(self)
        self.qle_file.resize(350, 25)
        self.qle_file.move(105, 50)
        self.qle_file.textChanged[str].connect(self.path_file_signal)

        lbl = QLabel(self)
        lbl.setText("File type")
        lbl.move(50, 100)

        file_type_combo = QComboBox(self)
        file_type_combo.addItems([".txt"])
        self.file_type = ".txt"
        file_type_combo.move(50, 120)
        file_type_combo.activated[str].connect(self.file_type_signal)


        self.model = QStandardItemModel(self)

        self.compression_type_combo = QComboBox(self)
        self.compression_type_combo.setModel(self.model)
        self.compression_type_combo.move(200,120)

        lbl = QLabel(self)
        lbl.setText("Type compression")
        lbl.move(200, 100)

        self.compression_subtype_combo = QComboBox(self)
        self.compression_subtype_combo.setModel(self.model)
        self.compression_subtype_combo.move(200, 180)

        lbl = QLabel(self)
        lbl.setText("Subype compression")
        lbl.move(200, 160)

        data = {
        'Lossless': ['Arithmetic coding'],
        'Lossy': ['Not yet']
        }

        self.pretype = 'Arithmetic coding'

        for k, v in data.items():
            state = QStandardItem(k)
            self.model.appendRow(state)
            for value in v:
                city = QStandardItem(value)
                state.appendRow(city)

        self.compression_type_combo.currentIndexChanged.connect(self.compression_type_signal)
        self.compression_type_signal(0)
        self.compression_subtype_combo.activated[str].connect(self.compression_subtype_signal)


        obtn = QPushButton('Open', self)
        obtn.clicked.connect(self.change_file_path)
        obtn.resize(obtn.sizeHint())
        obtn.move(20, 50)

        ebtn = QPushButton('Enocode', self)
        ebtn.clicked.connect(self.enc)
        ebtn.resize(ebtn.sizeHint())
        ebtn.move(20, 250)

        dbtn = QPushButton('Decode', self)
        dbtn.clicked.connect(self.dec)
        dbtn.resize(dbtn.sizeHint())
        dbtn.move(125, 250)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(395, 250)

        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle('ZUP')

        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def path_file_signal(self, text):
        self.path = text

    def file_type_signal(self, text):
        self.file_type = text

    def compression_type_signal(self, index):
        indx = self.model.index(index, 0, self.compression_type_combo.rootModelIndex())
        self.compression_subtype_combo.setRootModelIndex(indx)
        self.compression_subtype_combo.setCurrentIndex(0)

    def compression_subtype_signal(self, text):
        self.pretype = text

    def change_file_path(self):
        wb_patch = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', sys.argv[0])[0]
        self.qle_file.setText(wb_patch)
        self.path = wb_patch

    def enc(self):
        pass

    def dec(self):
        pass

    def open_file(self):
        f = open(self.path, 'r').read()
        return f



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())