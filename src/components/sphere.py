from components.vector import vec3, unit_vector
from math import pi, sqrt, inf
from components.color import *

class Sphere:
    def __init__(self, p, ce, r):
        self.p = p
        self.radius = r
        self.center = ce

    def intersect(self, start: vec3, direction: vec3, intersec: float):
        P = start - self.p
        a = vec3.dot(direction, direction)
        b = vec3.dot(P, direction) * 2
        c1 = vec3.dot(P, P) - self.radius * self.radius
        d = b * b - 4 * a * c1

        if d < 0:
            return 0

        dsc = 2.0 * a
        sqd = sqrt(d)

        intersec = (-b - sqd) / dsc

        if intersec > 0.1:
            return intersec

        intersec = (-b + sqd) / dsc
        if intersec > 0.1:
            return intersec

        return 0

def trace(spheres_count, O, distance, lights, spheres):
    h = -1
    T: float = 101118152822811797749760.0
    t = 10.0 ** 10

    for i in range(NS):
        if spheres[i].intersect(O, distance, T):
            T = spheres[i].intersect(O, distance, T)
            if t > T:
                t = T
                h = i

    if h > -1:
        p = O + distance * T
        n = unit_vector(p - spheres[h].p)
        r = distance - n * vec3.dot(distance, n) * 2
        c2 = spheres[h].center * 0.1

        if not h:
            spheres[h].center = vec3(1, 1, 1) if (int(p.x() + 10.0 ** 2) + int(p.z() + 10.0 ** 2)) & 1 else vec3(0, 0, 0)

        for j in range(NL):
            l1 = unit_vector(lights[j].p - p)
            sh = 0

            for i in range(NS):
                if spheres[i].intersect(p, l1, t):
                    sh = 1

            if not sh:
                df = max(0, vec3.dot(l1, n)) * 0.7
                sp = (max(0, vec3.dot(l1, n)) ** 50) * 0.3
                c2 = c2 + spheres[h].center * lights[j].center * df + vec3(sp, sp, sp)

        spheres_count = spheres_count - 1
        if spheres_count:
            c2 = c2 + trace(spheres_count, p, r, lights, spheres) * 0.51
        return c2

    return vec3(1 - distance.y(), 1 - distance.y(), 0.5 + distance.y())

spheres = [
    Sphere(vec3(0, -1000, 0), vec3(1, 1, 1), 1000),
    Sphere(vec3(-2.0, 1.0, 0.0), vec3(1, 0.0, 0.0), 1),
    Sphere(vec3(0.0, 0.8, 0.0), vec3(0.0, 1.0, 0.0), 0.8),
    Sphere(vec3(2.0, 10, -10.0), vec3(0.0, 0.0, 1.0), 0.6),
]

lights = [
    Sphere(vec3(0, 100, 0), vec3(0.0, 0.1, 0.2), 0),
    Sphere(vec3(100, 100, 200), vec3(0.3, 0.1, 0), 0),
    Sphere(vec3(-100, 100, 200), vec3(0.1, 0.3, 0.0), 0)
]

NS = 4
NL = 3