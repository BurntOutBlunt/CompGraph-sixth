from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QProgressBar, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from components.draw import Draw

class MainWindow(QMainWindow):
    WIDTH = 780
    HEIGHT = 660

    def __init__(self):
        super().__init__()
        self.logic = Draw()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Работа №6")
        self.setGeometry(100, 100, MainWindow.WIDTH, MainWindow.HEIGHT)

        # Main layout
        main_layout = QVBoxLayout()

        # Right frame
        self.frame_right = QFrame(self)
        right_layout = QVBoxLayout()
        self.frame_right.setLayout(right_layout)

        self.frame_info = QFrame(self.frame_right)
        info_layout = QVBoxLayout()
        self.frame_info.setLayout(info_layout)

        label_style = "background-color: #f5f5dc; color: black; border-radius: 6px; padding: 10px; font-size: 24px;"

        self.label_info_1 = QLabel("Прогресс обработки сцены", self.frame_info)
        self.label_info_1.setFont(QFont("Roboto Medium", 16))
        self.label_info_1.setAlignment(Qt.AlignCenter)
        self.label_info_1.setStyleSheet(label_style)
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
        self.entry_width.setText(self.logic.width_im)
        right_layout.addWidget(self.entry_width)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        right_layout.addLayout(buttons_layout)

        self.button_5 = QPushButton("Нарисовать сцену", self.frame_right)
        self.button_5.clicked.connect(self.draw_scene)
        buttons_layout.addWidget(self.button_5)

        self.button_2 = QPushButton("Обнулить значения", self.frame_right)
        self.button_2.clicked.connect(self.reset)
        buttons_layout.addWidget(self.button_2)

        self.button_exit = QPushButton("Выйти", self.frame_right)
        self.button_exit.clicked.connect(self.close)
        buttons_layout.addWidget(self.button_exit)

        # Add frames to main layout
        main_layout.addWidget(self.frame_right)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_sphere_inputs(self, grid):
        labels = ["x", "y", "z"]
        for i in range(3):
            for j in range(3):
                entry = QLineEdit(self.frame_right)
                entry.setText(self.logic.sph_c[i][j])
                grid.addWidget(QLabel(labels[j]), i, j * 2)
                grid.addWidget(entry, i, j * 2 + 1)

    def create_color_inputs(self, grid):
        labels = ["r", "g", "b"]
        for i in range(3):
            for j in range(3):
                entry = QLineEdit(self.frame_right)
                entry.setText(self.logic.sph_col[i][j])
                grid.addWidget(QLabel(labels[j]), i, j * 2)
                grid.addWidget(entry, i, j * 2 + 1)

    def draw_scene(self):
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

        width_im = int(self.entry_width.text())

        self.logic.apply(centers, colors, width_im)
        self.logic.write_to_image(self.progressbar)

    def reset(self):
        self.logic.reset()
        for i in range(3):
            for j in range(3):
                self.sphere_grid.itemAtPosition(i, j * 2 + 1).widget().setText(str(self.logic.sph_c[i][j]))
                self.sphere_color_grid.itemAtPosition(i, j * 2 + 1).widget().setText(str(self.logic.sph_col[i][j]))
        self.entry_width.setText(str(self.logic.width_im))
        self.update()
