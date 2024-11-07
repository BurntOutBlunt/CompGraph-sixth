import numpy as np

class vec3:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def normalize(self):
        n = self.__len__()
        if n > 0:
            nn = 1 / n
            self.e[0] *= nn
            self.e[1] *= nn
            self.e[2] *= nn
        return self

    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, item):
        return self.e[item]

    def __iadd__(self, other):
        self.e[0] += other.e[0]
        self.e[1] += other.e[1]
        self.e[2] += other.e[2]
        return self

    def __imul__(self, t: float):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self

    def __idiv__(self, t: float):
        return self.__imul__(1 / t)

    def __len__(self):
        return np.sqrt(self.length_squared())

    def length_squared(self):
        return self.e[0] ** 2 + self.e[1] ** 2 + self.e[2] ** 2

    def __repr__(self):
        return f'vec3({self.e[0]}, {self.e[1]}, {self.e[2]})'

    def __str__(self):
        return f'{self.e[0]} {self.e[1]} {self.e[2]}'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            x = self.e[0] + other.e[0]
            y = self.e[1] + other.e[1]
            z = self.e[2] + other.e[2]
            return vec3(x, y, z)
        elif isinstance(other, int):
            x = self.e[0] + other
            y = self.e[1] + other
            z = self.e[2] + other
            return vec3(x, y, z)
        elif isinstance(other, float):
            x = self.e[0] + other
            y = self.e[1] + other
            z = self.e[2] + other
            return vec3(x, y, z)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            x = self.e[0] - other.e[0]
            y = self.e[1] - other.e[1]
            z = self.e[2] - other.e[2]
            return vec3(x, y, z)
        elif isinstance(other, int):
            x = self.e[0] - other
            y = self.e[1] - other
            z = self.e[2] - other
            return vec3(x, y, z)
        elif isinstance(other, float):
            x = self.e[0] - other
            y = self.e[1] - other
            z = self.e[2] - other
            return vec3(x, y, z)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            x = self.e[0] * other.e[0]
            y = self.e[1] * other.e[1]
            z = self.e[2] * other.e[2]
            return vec3(x, y, z)
        elif isinstance(other, int):
            x = self.e[0] * other
            y = self.e[1] * other
            z = self.e[2] * other
            return vec3(x, y, z)
        elif isinstance(other, float):
            x = self.e[0] * other
            y = self.e[1] * other
            z = self.e[2] * other
            return vec3(x, y, z)

    def __rmul__(self, t: float):
        return self * t

    def __truediv__(self, t: float):
        return self * (1 / t)

    def cross(self, other):
        return vec3(self.e[1] * other.e[2] - self.e[2] * other.e[1],
                    self.e[2] * other.e[0] - self.e[0] * other.e[2],
                    self.e[0] * other.e[1] - self.e[1] * other.e[0])

    def dot(self, other):
        return self.e[0] * other.e[0] + self.e[1] * other.e[1] + self.e[2] * other.e[2]

def unit_vector(v: vec3):
    return v.__truediv__(v.__len__().real)

point3 = vec3
color = vec3
vect3 = vec3