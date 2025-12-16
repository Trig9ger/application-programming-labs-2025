import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

project_root = Path(__file__).parent.parent

lab2_path = project_root / 'pyproj2'
sys.path.insert(0, str(lab2_path))

from helpers import AnnotationIterator, annotation_check, write_csv

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Выбрать файл")
        self.button.setFixedSize(300, 40)
        self.button.clicked.connect(self.select_file)

        # Размещаем кнопку
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

        self.annotation_name = ""
        self.iterator = None
        self.path = None

        self.text = QLabel(self)
        self.image = QLabel(self)

        self.image_size = 0

        self.button_up = QPushButton("+")
        self.button_down = QPushButton("-")
        self.button_up.setFixedSize(100, 40)
        self.button_down.setFixedSize(100, 40)

        self.button_next = QPushButton("Next image!")
        self.button_delete = QPushButton("Delete this image!")



        self.image_scale_layout = QHBoxLayout()

        self.button_layout = QHBoxLayout()


    def select_file(self):
        self.annotation_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите CSV файл",
            "",
            "CSV файлы (*.csv);;Все файлы (*)"
        )


        self.iterator = iter(AnnotationIterator(self.annotation_name))

        #изображение и его название
        self.text = QLabel(self)
        self.image = QLabel(self)

        self.path = next(self.iterator)
        text = self.path[0].split('\\')[-1]
        image = QPixmap(self.path[0]).scaled(500, 500, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        self.text.setText(text)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setPixmap(image)



        #очищение
        self.layout.removeWidget(self.button)
        self.button.deleteLater()
        self.button = None

        #расположение
        self.layout.addWidget(self.text, alignment=QtCore.Qt.AlignBottom)

        self.image_scale_layout.addWidget(self.button_up, alignment=QtCore.Qt.AlignBottom)
        self.image_scale_layout.addWidget(self.button_down, alignment=QtCore.Qt.AlignBottom)
        self.layout.addLayout(self.image_scale_layout)

        self.layout.addWidget(self.image, alignment=QtCore.Qt.AlignCenter)

        self.button_layout.addWidget(self.button_next)
        self.button_layout.addWidget(self.button_delete)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.button_up.clicked.connect(self.scale_up)
        self.button_down.clicked.connect(self.scale_down)
        self.button_next.clicked.connect(self.next_img)
        self.button_delete.clicked.connect(self.delete_img)

    def scale_up(self):
        if self.image_size < 300:
            self.image_size += 100

        image = QPixmap(self.path[0]).scaled(500+self.image_size, 500+self.image_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(image)

    def scale_down(self):
        if self.image_size > -300:
            self.image_size -= 100

        image = QPixmap(self.path[0]).scaled(500+self.image_size, 500+self.image_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(image)

    def next_img(self):
        try:
            self.path = next(self.iterator)
            text = self.path[0].split('\\')[-1]
            image = QPixmap(self.path[0]).scaled(500, 500, aspectRatioMode = QtCore.Qt.KeepAspectRatio)

            self.text.setText(text)
            self.text.setAlignment(QtCore.Qt.AlignCenter)
            self.image.setPixmap(image)
            self.image_size = 0

        except StopIteration:
            self.iterator = iter(AnnotationIterator(self.annotation_name))
            self.path = next(self.iterator)
            text = self.path[0].split('\\')[-1]
            image = QPixmap(self.path[0]).scaled(500, 500, aspectRatioMode = QtCore.Qt.KeepAspectRatio)

            self.text.setText(text)
            self.text.setAlignment(QtCore.Qt.AlignCenter)
            self.image.setPixmap(image)
            self.image_size=0

    def delete_img(self):
        #удаляем изображение
        os.remove(self.path[0])

        #удаляем из csv
        directory_name = '\\'.join(self.path[0].split('\\')[:-1])

        write_csv(self.annotation_name, directory_name)

        #переходим на следующий элемент
        self.next_img()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        widget = MyWidget()
        widget.resize(1200, 900)
        widget.show()

        sys.exit(app.exec_())

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что указан правильный путь к файлу аннотации.")
        sys.exit(1)

    except ValueError as e:
        print(f"Ошибка: {e}")
        print("Файл аннотации должен быть в формате CSV.")
        sys.exit(1)

    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        print("Убедитесь, что у вас есть права на чтение файла аннотации.")
        sys.exit(1)

    except Exception as e:
        print(f"Неизвестная ошибка: {type(e).__name__}: {e}")
        print("Попробуйте проверить корректность данных в файле аннотации.")
        sys.exit(1)

