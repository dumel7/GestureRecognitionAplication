from __future__ import unicode_literals

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtWidgets import QLabel, QGridLayout


from BoxElement import BoxElement
from ChartBox import ChartBox
from PytorchModel import PytorchModel
from VideoBox import VideoBox
import numpy as np

class Application(QWidget):
    fileSignal = pyqtSignal(str, QTextEdit)
    imageSignal = pyqtSignal(QImage)
    chartSignal = pyqtSignal(np.ndarray)
    fileLabelSignal = pyqtSignal(str)
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
        self.pytorchModel = PytorchModel(self.chartSignal)
        self.pytorchModel.start()

        """set connections"""
        self.fileSignal.connect(self.pytorchModel.open_model)
        self.imageSignal.connect(self.pytorchModel.add_to_queue)
        self.chartSignal.connect(self.chartBox.fill_values)
        self.fileLabelSignal.connect(self.chartBox.make_char_labels)
        """set the layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.boxElement, alignment=Qt.AlignLeft)
        layout.addWidget(self.videoBox, alignment=Qt.AlignLeft)
        layout.addWidget(self.chartBox, alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec())