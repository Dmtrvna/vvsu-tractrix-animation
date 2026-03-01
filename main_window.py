import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QMessageBox, QComboBox
)
from PyQt5.QtCore import QTimer, QLocale
from PyQt5.QtGui import QDoubleValidator

from tractrix_calculator import TractrixCalculator
from matplotlib_widget import MatplotlibWidget


class MainWindow(QMainWindow):
    def __init__(self):
        """Инициализация главного окна приложения"""

        super().__init__()
        self.calculator = TractrixCalculator(a=3.0)
        self.current_plot_type = "cartesian"
        self.setWindowTitle("Трактриса — анимация в декартовой и полярной системах (PyQt5)")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.create_controls(main_layout)
        self.plot_widget = MatplotlibWidget()
        main_layout.addWidget(self.plot_widget)

        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_plot)
        self.update_plot()
        self.apply_styles()

    def create_controls(self, main_layout):
        """Создание элементов управления"""

        control_group = QGroupBox("Управление")
        control_layout = QHBoxLayout(control_group)

        label_a = QLabel("Параметр a (a > 2):")
        self.line_edit_a = QLineEdit("3.0")
        self.line_edit_a.setMaximumWidth(100)
        validator = QDoubleValidator(2.001, 100.0, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setLocale(QLocale(QLocale.C))
        self.line_edit_a.setValidator(validator)

        self.btn_apply = QPushButton("Применить")
        self.btn_apply.clicked.connect(self.update_plot)

        label_coord = QLabel("Система координат:")
        self.coord_combo = QComboBox()
        self.coord_combo.addItem("Декартова система")
        self.coord_combo.addItem("Полярная система")
        self.coord_combo.currentIndexChanged.connect(self.change_coord_system)

        self.btn_animation = QPushButton("Запустить анимацию")
        self.btn_animation.clicked.connect(self.toggle_animation)

        control_layout.addWidget(label_a)
        control_layout.addWidget(self.line_edit_a)
        control_layout.addWidget(self.btn_apply)
        control_layout.addWidget(label_coord)
        control_layout.addWidget(self.coord_combo)
        control_layout.addWidget(self.btn_animation)
        control_layout.addStretch()
        main_layout.addWidget(control_group)

    def apply_styles(self):
        """Применение стиля окна"""

        button_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """
        self.btn_animation.setStyleSheet(button_style)
        self.btn_apply.setStyleSheet(button_style)

    def change_coord_system(self, index):
        """Выбор системы координат"""

        self.current_plot_type = "cartesian" if index == 0 else "polar"
        self.update_plot()

    def update_plot(self):
        """Обновление графика"""

        try:
            a_text = self.line_edit_a.text()
            if not a_text:
                return
            a_value = float(a_text)
            if a_value <= 2:
                raise ValueError("Параметр a должен быть больше 2")
            self.calculator.set_parameter(a_value)
            self.plot_widget.plot_tractrix(self.calculator, self.current_plot_type)
            self.btn_animation.setText("Запустить анимацию")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка ввода", f"Некорректное значение: {str(e)}")

    def toggle_animation(self):
        """Смена значения кнопки анимации"""

        if not self.plot_widget.animation_running:
            self.start_animation()
        else:
            self.stop_animation()

    def start_animation(self):
        """Запуск анимации"""

        try:
            a_value = float(self.line_edit_a.text())
            if a_value <= 2:
                raise ValueError("Параметр a должен быть больше 2")
            self.plot_widget.start_animation(self.calculator, self.current_plot_type)
            self.btn_animation.setText("Остановить анимацию")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка анимации", str(e))

    def stop_animation(self):
        """Остановка анимации"""
        self.plot_widget.stop_animation()
        self.btn_animation.setText("Запустить анимацию")


def main():
    """Запуск программы"""

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

