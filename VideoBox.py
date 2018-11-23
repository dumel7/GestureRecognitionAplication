from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import cv2


class VideoBox(QWidget):
    def __init__(self, image_signal, parent=None):
        super().__init__(parent)
        self.imageSignal = image_signal
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 810
        self.image_rate = 0
        self.image_max_rate = 8
        self.title = 'Web camera video'
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(self.width)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        self.label = QLabel(self.title, self)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.image_rate += 1
        if self.image_rate == self.image_max_rate:
            self.image_rate = 0
            self.imageSignal.emit(image)


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __del__(self):
        self.wait()

    def run(self):
        self.setStackSize(200000000)
        # 0 fro the first device
        #cap = cv2.VideoCapture('VID_20180923_140835.mp4')
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.waitKey(150) #to 10 fps
                self.msleep(150)