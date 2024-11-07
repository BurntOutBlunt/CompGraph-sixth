import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QProgressBar, QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from vector import *
from color import *
from start import *
import numpy

class App(QMainWindow):
    WIDTH = 780
    HEIGHT = 660

    def __init__(self):
        super().__init__()

        self.x1 = "-3.0"
        self.y1 = "1.0"
        self.z1 = "1.0"
        self.x2 = "0.0"
        self.y2 = "1.0"
        self.z2 = "1.0"
        self.x3 = "2.0"
        self.y3 = "1.0"
        self.z3 = "1.0"
        self.sph_c = [
            [self.x1, self.y1, self.z1],
            [self.x2, self.y2, self.z2],
            [self.x3, self.y3, self.z3]
        ]

        self.r1 = "2.0"
        self.g1 = "2.0"
        self.b1 = "2.0"
        self.r2 = "1.0"
        self.g2 = "1.0"
        self.b2 = "1.0"
        self.r3 = "1.0"
        self.g3 = "2.0"
        self.b3 = "2.0"
        self.sph_col = [
            [self.r1, self.g1, self.b1],
            [self.r2, self.g2, self.b2],
            [self.r3, self.g3, self.b3]
        ]

        self.width_im = "100"
        self.height = int(self.width_im)
        self.width = int(self.height * 16.0 / 9.0)

        self.spheres = [
            Sphere(vect3(0, -1000, 0), vect3(1, 1, 1), 1000),
            Sphere(vect3(-3, 1, 1), vect3(2, 2, 2), 1),
            Sphere(vect3(0, 1, 1), vect3(1, 1, 1), 0.8),
            Sphere(vect3(2, 1, 1), vect3(1, 2, 2), 0.6),
        ]

        self.lights = [
            Sphere(vect3(0, 100, 0), vect3(0.0, 0.1, 0.2), 0),
            Sphere(vect3(100, 100, 200), vect3(0.3, 0.1, 0), 0),
            Sphere(vect3(-100, 100, 200), vect3(0.1, 0.3, 0.0), 0)
        ]

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Работа №6")
        self.setGeometry(100, 100, App.WIDTH, App.HEIGHT)

        # Main layout
        main_layout = QHBoxLayout()

        # Left frame
        self.frame_left = QFrame(self)
        self.frame_left.setFixedWidth(180)
        left_layout = QVBoxLayout()
        self.frame_left.setLayout(left_layout)

        self.label_1 = QLabel("Значения", self.frame_left)
        self.label_1.setFont(QFont("Roboto Medium", 16))
        left_layout.addWidget(self.label_1)

        self.button_1 = QPushButton("Обновить значения", self.frame_left)
        self.button_1.clicked.connect(self.apply)
        left_layout.addWidget(self.button_1)

        self.button_2 = QPushButton("Обнулить значения", self.frame_left)
        self.button_2.clicked.connect(self.reset)
        left_layout.addWidget(self.button_2)

        # Right frame
        self.frame_right = QFrame(self)
        right_layout = QVBoxLayout()
        self.frame_right.setLayout(right_layout)

        self.frame_info = QFrame(self.frame_right)
        info_layout = QVBoxLayout()
        self.frame_info.setLayout(info_layout)

        self.label_info_1 = QLabel("Загрузка...", self.frame_info)
        self.label_info_1.setFont(QFont("Roboto Medium", 16))
        self.label_info_1.setAlignment(Qt.AlignLeft)
        self.label_info_1.setStyleSheet("background-color: #9de0b4; color: black; border-radius: 6px;")
        info_layout.addWidget(self.label_info_1)

        self.progressbar = QProgressBar(self.frame_info)
        self.progressbar.setValue(0)
        info_layout.addWidget(self.progressbar)

        right_layout.addWidget(self.frame_info)

        # Sphere coordinates and color inputs
        self.sphere_label = QLabel("Введите координаты и радиус сфер", self.frame_right)
        self.sphere_label.setFont(QFont("Roboto Medium", 16))
        right_layout.addWidget(self.sphere_label)

        self.sphere_grid = QGridLayout()
        right_layout.addLayout(self.sphere_grid)

        self.create_sphere_inputs(self.sphere_grid)

        self.sphere_col_label = QLabel("Введите цвет сфер", self.frame_right)
        self.sphere_col_label.setFont(QFont("Roboto Medium", 16))
        right_layout.addWidget(self.sphere_col_label)

        self.sphere_color_grid = QGridLayout()
        right_layout.addLayout(self.sphere_color_grid)

        self.create_color_inputs(self.sphere_color_grid)

        self.sphere_col_label2 = QLabel("Высота изображения (16:9)", self.frame_right)
        self.sphere_col_label2.setFont(QFont("Roboto Medium", 16))
        right_layout.addWidget(self.sphere_col_label2)

        self.entry_width = QLineEdit(self.frame_right)
        self.entry_width.setText(self.width_im)
        right_layout.addWidget(self.entry_width)

        self.button_5 = QPushButton("Нарисовать сцену", self.frame_right)
        self.button_5.clicked.connect(self.write_to_image)
        right_layout.addWidget(self.button_5)

        # Add frames to main layout
        main_layout.addWidget(self.frame_left)
        main_layout.addWidget(self.frame_right)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_sphere_inputs(self, grid):
        labels = ["x", "y", "z"]
        for i in range(3):
            for j in range(3):
                entry = QLineEdit(self.frame_right)
                entry.setText(self.sph_c[i][j])
                grid.addWidget(QLabel(labels[j]), i, j * 2)
                grid.addWidget(entry, i, j * 2 + 1)

    def create_color_inputs(self, grid):
        labels = ["r", "g", "b"]
        for i in range(3):
            for j in range(3):
                entry = QLineEdit(self.frame_right)
                entry.setText(self.sph_col[i][j])
                grid.addWidget(QLabel(labels[j]), i, j * 2)
                grid.addWidget(entry, i, j * 2 + 1)

    def apply(self):
        centers = []
        for i in range(3):
            t = []
            for j in range(3):
                t.append(float(self.sphere_grid.itemAtPosition(i, j * 2 + 1).widget().text()))
            centers.append(t)

        colors = []
        for i in range(3):
            t = []
            for j in range(3):
                t.append(float(self.sphere_color_grid.itemAtPosition(i, j * 2 + 1).widget().text()))
            colors.append(t)

        self.height = int(self.entry_width.text())
        self.width = int(self.height * 16.0 / 9.0)

        for i in range(len(centers[0])):
            self.spheres[i + 1] = Sphere(vect3(centers[i][0], centers[i][1], centers[i][2]),
                                         vect3(colors[i][0], colors[i][1], colors[i][2]), abs(centers[i][1]))

    def reset(self):
        self.spheres = [
            Sphere(vect3(0, -1000, 0), vect3(1, 1, 1), 1000),
            Sphere(vect3(-3, 1, 1), vect3(2, 2, 2), 1),
            Sphere(vect3(0, 1, 1), vect3(1, 1, 1), 0.8),
            Sphere(vect3(2, 1, 1), vect3(1, 2, 2), 0.6),
        ]

        self.lights = [
            Sphere(vect3(0, 100, 0), vect3(0.0, 0.1, 0.2), 0),
            Sphere(vect3(100, 100, 200), vect3(0.3, 0.1, 0), 0),
            Sphere(vect3(-100, 100, 200), vect3(0.1, 0.3, 0.0), 0)
        ]

        c = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        col = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        w = 100

        for i in range(len(c)):
            for j in range(len(c[0])):
                self.sph_c[i][j] = c[i][j]
                self.sphere_grid.itemAtPosition(i, j * 2 + 1).widget().setText(str(c[i][j]))

        for i in range(len(col)):
            for j in range(len(col[0])):
                self.sph_col[i][j] = col[i][j]
                self.sphere_color_grid.itemAtPosition(i, j * 2 + 1).widget().setText(str(col[i][j]))

        self.entry_width.setText(str(w))
        self.update()

    def write_to_image(self):
        maxval = 255
        ppm_header = f'P6\n{self.width} {self.height}\n{maxval}\n'
        my_file = '/home/burntoutblunt/blue_red_example1.ppm'

        with open(my_file, 'wb') as f:
            f.write(bytearray(ppm_header, 'ascii'))

            for y in range(self.height):
                for x in range(self.width):
                    c = trace(len(self.spheres) - 1, vect3(0, 1, 5), unit_vector(vect3(x - self.width / 2,
                                                                                       self.height / 2.0 - y, -self.height)), self.lights, self.spheres)
                    pixel_col = vect3(int(min(1.0, c.x()) * 255.999),
                                      int(min(1.0, c.y()) * 255.999),
                                      int(min(1.0, c.z()) * 255.999))
                    write_color(my_file, pixel_col)

                self.progressbar.setValue(int((self.width * y) / (self.width * self.height) * 100))
                self.update()

        self.progressbar.setValue(100)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())