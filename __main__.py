from __future__ import unicode_literals

import datetime

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, QMutex, QWaitCondition, QThread
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout

from BoxElement import BoxElement
from ChartBox import ChartBox
from PytorchModel import PytorchModel
from VideoBox import VideoBox


class Application(QWidget):
    fileSignal = pyqtSignal(str)
    imageSignal = pyqtSignal(QImage, datetime.datetime)
    chartSignal = pyqtSignal(np.ndarray, datetime.datetime)
    fileLabelSignal = pyqtSignal(str)
    modelDescriptionSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()

    def interface(self):
        self.resize(1440, 810)
        self.setWindowTitle("Gesture Recognition Application")
        """set box elements"""
        self.boxElement = BoxElement(self.fileSignal, self.fileLabelSignal)
        self.videoBox = VideoBox(self.imageSignal)
        self.chartBox = ChartBox()

        """set pytorch model"""

        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.mThread = QThread()


        self.pytorchModel = PytorchModel(self.chartSignal, self.modelDescriptionSignal, self.cond, self.mutex)
        self.pytorchModel.moveToThread(self.mThread)
        self.mThread.finished.connect(self.pytorchModel.deleteLater)
        self.imageSignal.connect(self.pytorchModel.add_to_queue)
        self.mThread.start()

        """set connections"""
        self.fileSignal.connect(self.pytorchModel.open_model)
        self.imageSignal.connect(self.pytorchModel.add_to_queue)
        self.chartSignal.connect(self.chartBox.fill_values)
        self.fileLabelSignal.connect(self.chartBox.make_char_labels)
        self.modelDescriptionSignal.connect(self.boxElement.fillModelDescription)
        self.chartBox.waitSignal.connect(self.videoBox.th.updateWaitTime)
        """set the layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.boxElement, alignment=Qt.AlignLeft)
        layout.addWidget(self.videoBox, alignment=Qt.AlignLeft)
        layout.addWidget(self.chartBox, alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(100000)
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec())