import numpy as np


class TractrixCalculator:
    def __init__(self, a=2.5):
        """Инициализация переменных"""
        self.a = a

    def set_parameter(self, a):
        """Изменение параметра а"""
        self.a = a

    def cartesian_coordinates(self, t_values):
        """Вычисление координат трактрисы в декартовой системе"""
        x = self.a * (np.log(np.tan(t_values / 2)) + np.cos(t_values))
        y = self.a * np.sin(t_values)

        # [x, -x] - Левая и правая часть кривой
        return np.array([x, -x]), np.array(y)

    def polar_coordinates(self, t_values):
        """Вычисление координат трактрисы в полярной системе"""

        full_x, full_y = self.cartesian_coordinates(t_values)
        full_r = np.sqrt(full_x**2 + full_y**2)
        full_theta = np.arctan2(full_y, full_x)

        return np.array(full_r), np.array(full_theta)

    def get_full_animation_path_cartesian(self):
        """Получение полного пути анимации в декартовых координатах"""

        t_values = np.linspace(0.000001, np.pi / 2 - 0.000001, 200)
        x_pos, y_pos = self.cartesian_coordinates(t_values)

        x_full = np.concatenate((np.array([]), x_pos[0], x_pos[1]))
        y_full = np.concatenate((np.array([]), y_pos, y_pos))

        full_path = dict(zip(x_full, y_full))  # key + value
        sorted_x = sorted(full_path.keys())
        sorted_y = [full_path[key] for key in sorted_x]

        return sorted_x, sorted_y

    def get_full_animation_path_polar(self):
        """Получение полного пути анимации в полярных координатах"""
        t_values = np.linspace(0.01, np.pi / 2 - 0.01, 200)
        r_values, phi_values = self.polar_coordinates(t_values)

        # Объединяем левую и правую ветви
        r_full = np.concatenate((np.array([]), r_values[0], r_values[1]))
        phi_full = np.concatenate((np.array([]), phi_values[0], phi_values[1]))

        # Сортируем и объединяем
        full_tractrix = dict(zip(phi_full, r_full))  # key + value
        sorted_phi = sorted(full_tractrix.keys())
        sorted_r = [full_tractrix[key] for key in sorted_phi]

        return sorted_r, sorted_phi

