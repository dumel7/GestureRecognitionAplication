from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout
import csv

class ChartBox(QWidget):
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

    def fill_values(self, results):
        if self.fillValuesFlag:
            for i, value in enumerate(results):
                self.listQLineEdit[i].setText(value.__str__())

    def make_char_labels(self, path):
        layout = QFormLayout()
        with open(path, newline='\n') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                q_label = QLabel('Gest ' + row[0])
                q_line_edit = QLineEdit()
                q_line_edit.setReadOnly(True)
                layout.addRow(q_label, q_line_edit)
                self.listQLabel.append(q_label)
                self.listQLineEdit.append(q_line_edit)
        self.setLayout(layout)
        self.fillValuesFlag = True
