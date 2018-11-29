import os
import sys
from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleFactory, QPushButton, QFileDialog, QFrame


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(800, 500)
        self.file = None
        but = QPushButton("Choose a directory with images", self)
        but.move(300, 20)
        but.setFixedSize(200, 25)
        but.clicked.connect(lambda x: self.get_data_path())
        but.setFocusPolicy(Qt.NoFocus)

        self.left = QFrame(self)
        self.left.setFixedSize(200, 200)
        self.left.move(50, 150)
        self.left.setAutoFillBackground(False)
        self.left.setStyleSheet(
            "QFrame { background-color: transparent; background: url('green_ar.png') no-repeat left; background-size: 50px 50px;}")

        self.right = QFrame(self)
        self.right.setFixedSize(200, 200)
        self.right.move(550, 150)
        self.right.setAutoFillBackground(False)
        self.right.setStyleSheet(
            "QFrame { background-color: transparent; background: url('red_ar.png') no-repeat right; background-size: 50px 50px;}")

        self.img = QFrame(self)
        self.img.setFixedSize(200, 400)
        self.img.setFrameShadow(QFrame.Sunken)
        self.img.setFrameShape(QFrame.Panel)
        self.img.move(300, 50)
        self.img.setAutoFillBackground(False)

        self.show()

    def get_data_path(self):
        local_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if len(local_path) == 0: return
        self.local_path = local_path
        true_path = path.join(self.local_path, 'true')
        false_path = path.join(self.local_path, 'false')
        os.makedirs(true_path) if not os.path.exists(true_path) else None
        os.makedirs(false_path) if not os.path.exists(false_path) else None

        self.change_file()

    def change_file(self):
        self.first = os.listdir(self.local_path)[0]
        self.file = path.join(self.local_path, self.first).replace("\\", "/")
        self.img.setStyleSheet(
            "QFrame { background-color: transparent; background: url('"+self.file+"') no-repeat center; background-size: 100px 100px;}")

    def move_car(self, is_car):
        try:
            os.rename(self.file, path.join(self.local_path,
                                           "true" if is_car else "false",
                                           self.first
                                           )
                      )
            self.change_file()
        except:
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.move_car(True)
        elif event.key() == Qt.Key_Right:
            self.move_car(False)


if __name__ == "__main__":
    app = QApplication([])
    QApplication.setStyle(QStyleFactory.create("Windows"))
    window = MainWindow()
    sys.exit(app.exec_())