from vector import *
from math import pi, sqrt, inf
from color import *

class Sphere:
    def __init__(self, p, ce, r):
        self.p = p
        self.radius = r
        self.center = ce

    def intersect(self, start: vect3, direction: vect3, intersec: float):
        P = start - self.p
        a = vect3.dot(direction, direction)
        b = vect3.dot(P, direction) * 2
        c1 = vect3.dot(P, P) - self.radius * self.radius
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
        r = distance - n * vect3.dot(distance, n) * 2
        c2 = spheres[h].center * 0.1

        if not h:
            spheres[h].center = vect3(1, 1, 1) if (int(p.x() + 10.0 ** 2) + int(p.z() + 10.0 ** 2)) & 1 else vect3(0, 0, 0)

        for j in range(NL):
            l1 = unit_vector(lights[j].p - p)
            sh = 0

            for i in range(NS):
                if spheres[i].intersect(p, l1, t):
                    sh = 1

            if not sh:
                df = max(0, vect3.dot(l1, n)) * 0.7
                sp = (max(0, vect3.dot(l1, n)) ** 50) * 0.3
                c2 = c2 + spheres[h].center * lights[j].center * df + vect3(sp, sp, sp)

        spheres_count = spheres_count - 1
        if spheres_count:
            c2 = c2 + trace(spheres_count, p, r, lights, spheres) * 0.51
        return c2

    return vect3(1 - distance.y(), 1 - distance.y(), 0.5 + distance.y())

spheres = [
    Sphere(vect3(0, -1000, 0), vect3(1, 1, 1), 1000),
    Sphere(vect3(-2.0, 1.0, 0.0), vect3(1, 0.0, 0.0), 1),
    Sphere(vect3(0.0, 0.8, 0.0), vect3(0.0, 1.0, 0.0), 0.8),
    Sphere(vect3(2.0, 10, -10.0), vect3(0.0, 0.0, 1.0), 0.6),
]

lights = [
    Sphere(vect3(0, 100, 0), vect3(0.0, 0.1, 0.2), 0),
    Sphere(vect3(100, 100, 200), vect3(0.3, 0.1, 0), 0),
    Sphere(vect3(-100, 100, 200), vect3(0.1, 0.3, 0.0), 0)
]

NS = 4
NL = 3

if __name__ == '__main__':
    ext = 16.0 / 9.0
    H = 150
    W = int(H * ext)
    maxval = 255

    ppm_header = f'P6\n{W} {H}\n{maxval}\n'
    my_file = 'blue_red_example1.ppm'

    with open(my_file, 'wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))

        for y in range(H):
            for x in range(W):
                c = trace(len(spheres) - 1, vect3(0, 1, 5), unit_vector(vect3(x - W / 2, H / 2.0 - y, -H)), lights, spheres)
                pixel_col = vect3(int(min(1.0, c.x()) * 255), int(min(1.0, c.y()) * 255), int(min(1.0, c.z()) * 255))
                write_color(my_file, pixel_col)