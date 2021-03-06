import csv
import datetime

import numpy as np
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QTextEdit, QVBoxLayout


class ChartBox(QWidget):
    MAX_DELAY = 10
    MIN_DELAY = 1
    waitSignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 810
        self.listQLabel = []
        self.listQLineEdit = []
        self.init_ui()
        self.fillValuesFlag = False


    def init_ui(self):
        self.setFixedWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)


    @pyqtSlot(np.ndarray, datetime.datetime)
    def fill_values(self, results, time):
        if self.fillValuesFlag:
            for i, value in enumerate(results):
                self.listQLineEdit[i].setText(value.__str__())
            indx = np.argmax(results)
            delay = datetime.datetime.now() - time
            if delay.seconds > self.MAX_DELAY:
                self.waitSignal.emit(-1)
            if delay.seconds < self.MIN_DELAY:
                self.waitSignal.emit(1)
            self.datetime.setText(delay.__str__())
            if indx != self.currentGest:
                self.currentGest = indx
                self.details.setText(self.details.toPlainText() + '\n' + self.listQLabel[self.currentGest].text() + "\t:\t" + results[indx].__str__())
            #QApplication.processEvents()


    def make_char_labels(self, path):
        layout = QFormLayout()
        with open(path, newline='\n') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                q_label = QLabel(row[0])
                q_line_edit = QLineEdit()
                q_line_edit.setReadOnly(True)
                layout.addRow(q_label, q_line_edit)
                self.listQLabel.append(q_label)
                self.listQLineEdit.append(q_line_edit)
        self.currentGest = -1
        self.datetimeLabel = QLabel('Delay')
        self.datetime = QLineEdit()
        layout.addRow(self.datetimeLabel, self.datetime)

        layout2 = QVBoxLayout()
        layout2.addLayout(layout)
        self.details = QTextEdit()
        self.details.setEnabled(False)
        layout2.addWidget(self.details)
        self.setLayout(layout2)
        self.fillValuesFlag = True
