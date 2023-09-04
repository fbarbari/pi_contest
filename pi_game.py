import math
from random import uniform


def random_coords():
    return (uniform(-1, +1), uniform(-1, +1))


class PiGame(object):
    def __init__(self):
        self.m_total = 0
        self.m_inside = 0
        self.throw_coords()

    def add(self):
        self.m_total = self.m_total + 1
        if self.inside():
            self.m_inside = self.m_inside + 1

    def value(self):
        try:
            return float(self.m_inside) / self.m_total * 4.0
        except BaseException:
            return float("nan")

    def error(self):
        return abs(math.pi - self.value()) / math.pi * 100.0

    def throw_coords(self):
        self.m_coords = random_coords()
        return self.m_coords

    def coords(self):
        return self.m_coords

    def inside(self):
        x = self.m_coords[0]
        y = self.m_coords[1]

        return x**2 + y**2 < 1
