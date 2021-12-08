from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> str:
        """Получить данные тренировки."""
        return self.MESSAGE.format(
            self.training_type, self.duration, self.distance, self.speed, self.calories
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUNNING_1: int = 18
    COEFF_CALORIE_RUNNING_2: int = 20
    HOUR_IN_MIN: int = 60

    def get_spent_calories(self) -> float:
        """Получить число потраченных калорий."""
        mean_speed = self.get_mean_speed()
        return (
            (self.COEFF_CALORIE_RUNNING_1 * mean_speed - self.COEFF_CALORIE_RUNNING_2)
            * self.weight
            / self.M_IN_KM
            * self.HOUR_IN_MIN
            * self.duration
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_SPORTS_WALKING_1: float = 0.035
    COEFF_CALORIE_SPORTS_WALKING_2: float = 0.029
    HOUR_IN_MIN: int = 60

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить число потраченных калорий."""
        speed = self.get_mean_speed()
        return (
            (
                self.COEFF_CALORIE_SPORTS_WALKING_1 * self.weight
                + speed ** 2
                // self.height
                * self.COEFF_CALORIE_SPORTS_WALKING_2
                * self.weight
            )
            * self.HOUR_IN_MIN
            * self.duration
        )


class Swimming(Training):
    """Тренировка: плавание."""

    COEFF_CALORIE_SWIMMING_1: float = 1.1
    COEFF_CALORIE_SWIMMING_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить число потраченных калорий."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_SWIMMING_1)
            * self.COEFF_CALORIE_SWIMMING_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    decoding_trainings = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    if workout_type in decoding_trainings:
        return decoding_trainings.get(workout_type)(*data)
    ValueError("Неизвестный тип тренировки")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
