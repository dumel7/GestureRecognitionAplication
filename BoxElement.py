from PyQt5.QtCore import pyqtSlot, QLine, Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, \
    QBoxLayout, QLabel, QTextEdit


class BoxElement(QWidget):
    def __init__(self, fileSignal, parent=None):
        super().__init__(parent)
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 810
        self.filePathBox = QLineEdit()
        self.openButton = QPushButton('open')
        self.details = QTextEdit()
        self.detailsName = QLabel()
        self.init_ui()
        self.fileSignal = fileSignal

    def init_ui(self):
        self.setFixedWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.details.setReadOnly(True)
        self.detailsName.setText('Model\'s Details')
        self.details.setFixedHeight(800)
        layout = QVBoxLayout()
        layout.addWidget(self.init_open_element(), alignment=Qt.AlignTop)
        layout.addWidget(self.detailsName, alignment=Qt.AlignTop)
        layout.addWidget(self.details, alignment=Qt.AlignTop)
        self.setLayout(layout)


    def init_open_element(self):
        widget = QWidget()
        self.filePathBox.setFixedWidth(300)
        layout = QFormLayout(widget)
        layout.addRow(self.filePathBox, self.openButton)
        self.openButton.setToolTip('Choose the model')
        self.openButton.clicked.connect(self.open_file_name_dialog)
        return widget

    def open_file_name_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a model", "", "PyTorch Files (*.pth.tar)")
        self.filePathBox.setText(file_name.__str__())
        self.filePathBox.displayText()
        if file_name != '':
            self.fileSignal.emit()

    def path(self):
        return self.filePathBox.text()
