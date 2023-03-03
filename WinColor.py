from random import randint


class WinColor:
    def __init__(self):
        self.r, self.g, self.b = 0, 0, 0

    def get_color(self):
        return self.r, self.g, self.b

    def random_color(self):
        self.r = randint(0, 150)
        self.g = randint(0, 150)
        self.b = randint(0, 150)

    def dim_color(self):
        if self.r > 0:
            self.r -= 1
        if self.g > 0:
            self.g -= 1
        if self.b > 0:
            self.b -= 1
