import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPixmap

project_root = Path(__file__).parent.parent

lab2_path = project_root / 'pyproj2'
sys.path.insert(0, str(lab2_path))

from helpers import AnnotationIterator, annotation_check, write_csv

class MyWidget(QWidget):
    def __init__(self, annotation_name: str):
        super().__init__()

        self.annotation_name = annotation_name
        self.iterator = iter(AnnotationIterator(annotation_name))

        #изображение и его название
        self.text = QLabel(self)
        self.image = QLabel(self)

        self.path = next(self.iterator)
        text = self.path[0].split('\\')[-1]
        image = QPixmap(self.path[0]).scaled(400, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        с = 1

        self.text.setText(text)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setPixmap(image)

        #кнопки для итерации и удаления текущего изображения
        self.button_next = QPushButton("Next image!")
        self.button_delete = QPushButton("Delete this image!")

        #расположение
        self.layout = QVBoxLayout()

        self.image_layout = QHBoxLayout()
        self.image_layout.addWidget(self.text)
        self.image_layout.addWidget(self.image)

        self.layout.addLayout(self.image_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_next)
        self.button_layout.addWidget(self.button_delete)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.button_next.clicked.connect(self.next_img)
        self.button_delete.clicked.connect(self.delete_img)

    def next_img(self):
        try:
            self.path = next(self.iterator)
            text = self.path[0].split('\\')[-1]
            image = QPixmap(self.path[0]).scaled(400, 300, aspectRatioMode = QtCore.Qt.KeepAspectRatio)

            self.text.setText(text)
            self.text.setAlignment(QtCore.Qt.AlignCenter)
            self.image.setPixmap(image)
        except StopIteration:
            self.iterator = iter(AnnotationIterator(self.annotation_name))

    def delete_img(self):
        #удаляем изображение
        os.remove(self.path[0])

        #удаляем из csv
        directory_name = '\\'.join(self.path[0].split('\\')[:-1])

        write_csv(self.annotation_name, directory_name)

        #переходим на следующий элемент
        self.next_img()