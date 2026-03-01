import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QMessageBox)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        """Инициализация виджета и переменных"""

        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = None
        self.square = None
        self.animation = None
        self.animation_running = False

    def setup_plot(self, plot_type):
        """Настройка графика"""

        self.figure.clear()
        if plot_type == "cartesian":
            self.ax = self.figure.add_subplot(111)
            self.ax.grid(True, alpha=0.3)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Трактриса в декартовых координатах')
            self.ax.axhline(y=0, color='k', linewidth=0.5)
            self.ax.axvline(x=0, color='k', linewidth=0.5)
            self.ax.set_aspect('equal')
        elif plot_type == "polar":
            self.ax = self.figure.add_subplot(111, projection='polar')
            self.ax.grid(True, alpha=0.3)
            self.ax.set_title('Трактриса в полярных координатах')

    def plot_tractrix(self, calculator, plot_type):
        """Отображение трактрисы"""
        self.setup_plot(plot_type)

        if plot_type == "cartesian":
            t_values = np.linspace(0.000001, np.pi / 2 - 0.000001, 1000)
            x_pos, y_pos = calculator.cartesian_coordinates(t_values)

            self.ax.plot(x_pos[0], y_pos, 'r-', linewidth=2, label='Кривая Трактриса')
            self.ax.plot(x_pos[1], y_pos, 'r-', linewidth=2)
            self.ax.legend()
            self.ax.set_xlim(-calculator.a * 1.5, calculator.a * 1.5)
            self.ax.set_ylim(-0.5, calculator.a * 1.5)

        else:  # polar
            t_values = np.linspace(0.01, np.pi - 0.01, 500)
            r_values, phi_values = calculator.polar_coordinates(t_values)

            if len(r_values) > 0:
                # Объединяем левую и правую ветви в одну кривую
                r_full = np.concatenate((np.array([]), r_values[0], r_values[1]))
                phi_full = np.concatenate((np.array([]), phi_values[0], phi_values[1]))

                # Сортируем и объединяем
                full_tractrix = dict(zip(phi_full, r_full))  # key + value
                sorted_phi = sorted(full_tractrix.keys())
                sorted_r = [full_tractrix[key] for key in sorted_phi]

                # Строим одну кривую
                self.ax.plot(sorted_phi, sorted_r, 'r-', linewidth=2, label='Кривая Трактриса')
                self.ax.legend()

        self.canvas.draw()

    def start_animation(self, calculator, plot_type):
        """Старт анимации"""

        self.stop_animation()
        if plot_type == "cartesian":
            self._start_cartesian_animation(calculator)
        else:
            self._start_polar_animation(calculator)

    def _start_cartesian_animation(self, calculator):
        """Запуск анимации в декартовых координатах"""

        x_path, y_path = calculator.get_full_animation_path_cartesian()
        square_size = max(0.15, calculator.a / 10)
        self.square = patches.Rectangle(
            (x_path[0] - square_size / 2, y_path[0] - square_size / 2),
            square_size, square_size,
            linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.7, label='Движущаяся точка'
        )
        self.ax.add_patch(self.square)

        def animate(frame):
            if frame < len(x_path):
                self.square.set_xy((x_path[frame] - square_size / 2, y_path[frame] - square_size / 2))
            return [self.square]

        self.animation = FuncAnimation(
            self.figure, animate, frames=len(x_path),
            interval=30, blit=True, repeat=True
        )
        self.animation_running = True
        self.canvas.draw()

    def _start_polar_animation(self, calculator):
        """Запуск анимации в полярных координатах"""

        r_path, phi_path = calculator.get_full_animation_path_polar()
        if len(r_path) == 0:
            QMessageBox.warning(None, "Ошибка", "Не удалось вычислить траекторию для полярной анимации")
            return

        square_size = max(0.15, calculator.a / 10)
        self.square = patches.Rectangle(
            (phi_path[0] - square_size / 2, r_path[0] - square_size / 2),
            square_size, square_size,
            linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.7, label='Движущаяся точка'
        )
        self.ax.add_patch(self.square)

        def animate(frame):
            current_phi = phi_path[frame]
            current_r = r_path[frame]
            self.square.set_xy((current_phi - square_size / 2, current_r - square_size / 2))
            return self.square,

        self.animation = FuncAnimation(
            self.figure, animate, frames=len(r_path),
            interval=30, blit=True, repeat=True
        )
        self.animation_running = True
        self.canvas.draw()

    def stop_animation(self):
        """Остановка анимации"""

        if self.animation:
            self.animation.event_source.stop()
            self.animation = None
        if self.square:
            self.square.remove()
            self.square = None

        self.animation_running = False
        self.canvas.draw()


