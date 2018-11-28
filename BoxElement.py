from PyQt5.QtCore import pyqtSlot, QLine, Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, \
    QBoxLayout, QLabel, QTextEdit


class BoxElement(QWidget):
    def __init__(self, fileSignal, fileLabelSignal, parent=None):
        super().__init__(parent)
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 810
        self.filePathBox = QLineEdit()
        self.openButton = QPushButton('open model')
        self.labelPathBox = QLineEdit()
        self.openLabelButton = QPushButton('open labels')
        self.details = QTextEdit()
        self.detailsName = QLabel()
        self.init_ui()
        self.fileSignal = fileSignal
        self.fileLabelSignal = fileLabelSignal

    def init_ui(self):
        self.setFixedWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.details.setReadOnly(True)
        self.detailsName.setText('Model\'s Details')
        self.details.setFixedHeight(800)
        layout = QVBoxLayout()
        layout.addWidget(self.init_open_model(), alignment=Qt.AlignTop)
        layout.addWidget(self.detailsName, alignment=Qt.AlignTop)
        layout.addWidget(self.details, alignment=Qt.AlignTop)
        self.setLayout(layout)


    def init_open_model(self):
        widget = QWidget()
        self.filePathBox.setFixedWidth(300)
        self.labelPathBox.setFixedWidth(300)
        layout = QFormLayout(widget)
        layout.addRow(self.filePathBox, self.openButton)
        layout.addRow(self.labelPathBox, self.openLabelButton)

        self.openButton.setToolTip('Choose the model')
        self.openButton.clicked.connect(self.open_file_name_dialog)

        self.openLabelButton.setToolTip('Choose the labels')
        self.openLabelButton.clicked.connect(self.open_file_label)
        return widget


    def open_file_name_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a model", "", "PyTorch Files (*.pth.tar)")
        self.filePathBox.setText(file_name.__str__())
        self.filePathBox.displayText()
        if file_name != '':
            self.fileSignal.emit(file_name)

    def open_file_label(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a label file", "", "CSV files (*.csv)")
        self.labelPathBox.setText(file_name.__str__())
        self.labelPathBox.displayText()
        if file_name != '':
            self.fileLabelSignal.emit(file_name)

    def fillModelDescription(self, details):
        self.details.setText(details)

    def path(self):
        return self.filePathBox.text()
