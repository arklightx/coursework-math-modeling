import sys
import statistics as stat
from collections import Counter
from termcolor import colored

ARR_NAME: dict = {
    "1": colored("GeForce GTX 1050 Ti", "green"),
    "2": colored("GeForce GTX 1660 super", "green"),
    "3": colored("GeForce RTX 2060 super", "green"),
    "4": colored("GeForce RTX 3070", "green")
}


class Nerv:
    array: list[list[float]]
    vector: list[float]
    n: int

    def __init__(self, array: list[list[float]], vector: list[float]):
        self.array = array
        self.vector = vector
        self.n = len(array)

        if len(array) == 0 or len(array[0]) == 0:
            raise Exception("Дан пустой массив.")

        self.__enter_priority()

    def get_laplace_criteria(self) -> int:
        """Возвращает индекс видеокарты по критерию Лапласа

        Формируется вектор, в котором находятся средние значения критериев
        соответственных видеокарт. Дальше находится максимум, который и будет
        критерием Лапласа

        :return: index - номер видеокарты в человеческом представлении
        """
        weight_vector: list[float] = [stat.mean(self.array[i]) for i in range(self.n)]
        index: int = weight_vector.index(max(weight_vector)) + 1
        self.print_result("Лапласа", weight_vector, index)
        return index

    def get_wald_criteria(self) -> int:
        """Возвращает индекс видеокарты по критерию Вальда

        Формируется вектор, в котором находятся наименьшие критерие от каждой
        видеокарты. Дальше, среди наихудших критериев выбирается наибольший.
        Выбранный критерий будет отображать критерий Вальда

        :return: index - номер видеокарты в человеческом представлении
        """
        weight_vector: list[float] = [min(self.array[i]) for i in range(self.n)]
        index: int = weight_vector.index(max(weight_vector)) + 1
        self.print_result("Вальда", weight_vector, index)
        return index

    def get_savage_criteria(self) -> int:
        """Возвращает индекс видеокарты по критерию Сэвиджа

        Выбираются максимальные критерии от каждой видеокарты. Дальше формируется
        матрица рисков. Из матрицы рисков выбираются самые ненадёжные случаи (
        максимальные риски). После этого, среди худших рисков отбираются наименьшие

        :return: index - номер видеокарты в человеческом представлении
        """
        max_list: list[float] = [max(self.array[i]) for i in range(self.n)]  # 1
        diff_list: list[list[float]] = []  # 2
        for i in range(self.n):
            diff_list.append([(max_list[i] - self.array[i][j]) for j in range(len(self.array[i]))])
        weight_vector: list[float] = [max(diff_list[i]) for i in range(len(diff_list))]
        index: int = weight_vector.index(min(weight_vector)) + 1
        self.print_result("Сэвиджа", weight_vector, index)
        return index

    def get_hurwitz_criteria(self, a: float) -> int:
        """Возвращает индекс видеокарты по критерию Гурвица

        Формируются списки лучших и худших критериев, дальше формируется
        вектор весов по формуле Гурвица на основе параметра позитивности. Максимум
        из вектора весов покажет критерий Гурвица.

        :param a: параметр позитивности [0;1]
        :return: index - номер видеокарты в человеческом представлении
        """
        max_list: list[float] = [max(self.array[i]) for i in range(self.n)]
        min_list: list[float] = [min(self.array[i]) for i in range(self.n)]
        weight_vector: list[float] = [(max_list[i] * a + (1 - a) * min_list[i]) for i in range(self.n)]
        index: int = weight_vector.index(max(weight_vector)) + 1
        self.print_result(f"Гурвица({a})", weight_vector, index)
        return index

    @staticmethod
    def print_result(method: str, vector_weight: list[float], index: int) -> None:
        """Красивый вывод на экран

        :param method: название метода в родительном падеже
        :param vector_weight: вектор весов
        :param index: индекс видеокарты в ARR_NAME
        """
        print(f"Критерий {method}:", end=" ")
        print(vector_weight)
        print(f"    Наилучший вариант: {ARR_NAME[str(index)]}.",)
        print(f"    Индекс элемента: {colored(index, 'green')}.")

    def __enter_priority(self) -> None:
        """Применение вектора приоритетов на заданный массив"""
        for i in range(self.n):
            for j in range(len(self.array[i])):
                self.array[i][j] *= self.vector[j]


if __name__ == '__main__':
    arr = [
        [1, 0.4, 0.5, 0.4, 0.4, 0.15],
        [0.5, 0.7, 0.8, 0.8, 0.7, 0.3],
        [0.4, 0.7, 1, 0.8, 0.9, 0.5],
        [0.1, 1, 1, 0.8, 0.9, 0.9]
    ]
    vector_priority = [
        [0, 0.9, 1, 0.9, 1, 1],  # геймер
        [1, 0.1, 0.2, 0.01, 0.0001, 0.4],  # офисный работник
        [0.7, 0.5, 0.8, 0.4, 0.3, 0.7]  # студент
    ]
    arr_criteria = []
    current_vector = vector_priority[0]
    print("Текущий вектор приоритетов: ", end=" ")
    print(current_vector)
    nerv = Nerv(arr, current_vector)
    arr_criteria.append(nerv.get_laplace_criteria())  # лучший вариант при самом благоприятном исходе
    arr_criteria.append(nerv.get_wald_criteria())  # худший из возможных исходов
    arr_criteria.append(nerv.get_savage_criteria())  # максимально недополученный выигрыш или минимальный выигрыш
    arr_criteria.append(nerv.get_hurwitz_criteria(0))  # полный пессимизм
    arr_criteria.append(nerv.get_hurwitz_criteria(0.5))  # полу-пессимиз
    arr_criteria.append(nerv.get_hurwitz_criteria(1))  # оптимизм
    counter = Counter(arr_criteria)
    card = counter.most_common()[0][0]
    repeated = counter.most_common()[0][1]
    print(f"Наиболее предпочтительная карта: {ARR_NAME[str(card)]}. Подошла по {colored(repeated, 'green')} критер.")
    sys.exit(0)
