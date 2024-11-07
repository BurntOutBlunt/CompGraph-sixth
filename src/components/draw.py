from components.vector import vec3
from components.color import *
from components.sphere import *

class Draw:
    def __init__(self):
        self.x1 = "-3.0"
        self.y1 = "1.0"
        self.z1 = "1.0"
        self.x2 = "0.0"
        self.y2 = "1.0"
        self.z2 = "1.0"
        self.x3 = "2.0"
        self.y3 = "1.0"
        self.z3 = "1.0"
        self.sph_c = [
            [self.x1, self.y1, self.z1],
            [self.x2, self.y2, self.z2],
            [self.x3, self.y3, self.z3]
        ]

        self.r1 = "2.0"
        self.g1 = "2.0"
        self.b1 = "2.0"
        self.r2 = "1.0"
        self.g2 = "1.0"
        self.b2 = "1.0"
        self.r3 = "1.0"
        self.g3 = "2.0"
        self.b3 = "2.0"
        self.sph_col = [
            [self.r1, self.g1, self.b1],
            [self.r2, self.g2, self.b2],
            [self.r3, self.g3, self.b3]
        ]

        self.width_im = "100"
        self.height = int(self.width_im)
        self.width = int(self.height * 16.0 / 9.0)

        self.spheres = [
            Sphere(vec3(0, -1000, 0), vec3(1, 1, 1), 1000),
            Sphere(vec3(-3, 1, 1), vec3(2, 2, 2), 1),
            Sphere(vec3(0, 1, 1), vec3(1, 1, 1), 0.8),
            Sphere(vec3(2, 1, 1), vec3(1, 2, 2), 0.6),
        ]

        self.lights = [
            Sphere(vec3(0, 100, 0), vec3(0.0, 0.1, 0.2), 0),
            Sphere(vec3(100, 100, 200), vec3(0.3, 0.1, 0), 0),
            Sphere(vec3(-100, 100, 200), vec3(0.1, 0.3, 0.0), 0)
        ]

    def apply(self, centers, colors, width_im):
        self.height = int(width_im)
        self.width = int(self.height * 16.0 / 9.0)

        for i in range(len(centers[0])):
            self.spheres[i + 1] = Sphere(vec3(centers[i][0], centers[i][1], centers[i][2]),
                                         vec3(colors[i][0], colors[i][1], colors[i][2]), abs(centers[i][1]))

    def reset(self):
        self.spheres = [
            Sphere(vec3(0, -1000, 0), vec3(1, 1, 1), 1000),
            Sphere(vec3(-0, 0, 0), vec3(0, 0,0), 1),
            Sphere(vec3(0, 0, 0), vec3(0, 0, 0), 0.8),
            Sphere(vec3(0, 0, 0), vec3(0, 0, 0), 0.6),
        ]

        self.lights = [
            Sphere(vec3(0, 100, 0), vec3(0.0, 0.1, 0.2), 0),
            Sphere(vec3(100, 100, 200), vec3(0.3, 0.1, 0), 0),
            Sphere(vec3(-100, 100, 200), vec3(0.1, 0.3, 0.0), 0)
        ]

        c = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        col = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        w = 100

        for i in range(len(c)):
            for j in range(len(c[0])):
                self.sph_c[i][j] = c[i][j]

        for i in range(len(col)):
            for j in range(len(col[0])):
                self.sph_col[i][j] = col[i][j]

        self.width_im = str(w)

    def write_to_image(self, progressbar):
        maxval = 255
        ppm_header = f'P6\n{self.width} {self.height}\n{maxval}\n'
        my_file = '/home/burntoutblunt/blue_red_example1.ppm'

        with open(my_file, 'wb') as f:
            f.write(bytearray(ppm_header, 'ascii'))

            for y in range(self.height):
                for x in range(self.width):
                    c = trace(len(self.spheres) - 1, vec3(0, 1, 5), unit_vector(vec3(x - self.width / 2,
                                                                                       self.height / 2.0 - y, -self.height)), self.lights, self.spheres)
                    pixel_col = vec3(int(min(1.0, c.x()) * 255.999),
                                      int(min(1.0, c.y()) * 255.999),
                                      int(min(1.0, c.z()) * 255.999))
                    write_color(my_file, pixel_col)

                progressbar.setValue(int((self.width * y) / (self.width * self.height) * 100))
                progressbar.update()

        progressbar.setValue(100)
        progressbar.update()