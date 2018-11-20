from __future__ import unicode_literals

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout

from BoxElement import BoxElement
from PytorchModel import PytorchModel


class Application(QWidget):
    fileSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()

    def interface(self):
        self.resize(1440, 810)
        self.setWindowTitle("Gesture Recognition Application")
        self.boxElement = BoxElement(self.fileSignal)
        self.fileSignal.connect(self.open_model)

        layout = QHBoxLayout()
        layout.addWidget(self.boxElement, alignment=Qt.AlignLeft)


        self.setLayout(layout)
        self.show()

    def open_model(self):
        self.pytorchModel = PytorchModel(self.boxElement.path())
        self.boxElement.details.setText(self.pytorchModel.get_model_details())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec())