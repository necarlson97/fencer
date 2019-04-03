import math


class Point():

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def adde(self, p):
        # plus equals
        self.x += p.x
        self.y += p.y
        return self

    def add(self, p):
        # plus (returning new)
        return self.copy().adde(p)

    def sube(self, p):
        # minus equals
        self.y -= p.y
        self.x -= p.x
        return self

    def sub(self, p):
        # minus (returning new)
        return self.copy().sube(p)

    def multe(self, p):
        # multiply equals
        self.y *= p.y
        self.x *= p.x
        return self

    def mult(self, p):
        # minus (returning new)
        return self.copy().multe(p)

    def abse(self):
        # absolute value on self
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self

    def abs(self):
        # absolute value (returning new)
        return self.copy().abse()

    def powe(self, n=2):
        # power on self
        self.x **= n
        self.y **= n
        return self

    def pow(self, n=2):
        # power (returning new)
        return self.copy().powe(n)

    def set(self, x=0, y=0):
        # set point to x, y
        self.x = x
        self.y = y
        return self

    def setp(self, p):
        # set point to x, y from a point
        self.x = p.x
        self.y = p.y
        return self

    def dist(self, tx, ty):
        # distance between self and x, y
        dx = tx - self.x
        dy = ty - self.y
        return math.sqrt(dx**2 + dy**2)

    def distp(self, p):
        # distance betwen self and another point
        return self.dist(p.x, p.y)

    def mag(self, p):
        # magnitude
        p1 = self.sub(p).pow()
        return math.sqrt(p1.x + p1.y)

    def copy(self):
        return Point(self.x, self.y)

    def tup(self):
        # Tuple of reals
        return (self.x, self.y)

    def int(self):
        # Tuple of ints (useful for drawing)
        return (int(self.x), int(self.y))

    def __repr__(self):
        # TODO not really a repr
        return f'{self.int()}'

    def __str__(self):
        return self.__repr__()
