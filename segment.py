import math

import pygame as pg

from point import Point


def cart_to_polar(p, angle, length):
    polx = length * math.cos(angle)
    poly = length * math.sin(angle)
    r = Point(polx, poly).add(p)
    return r


class Segment():

    count = 0

    # a is the root
    # b is the tip

    def __init__(self, parent=None, length=20, angle=0):
        self.b = Point()
        self.angle = angle
        self.length = length

        if parent:
            self.a = parent.b
            self.parent = parent
        else:
            self.a = Point()
            self.parent = None

        self.id = Segment.count
        Segment.count += 1

    def cart_to_polar(self, p=None, angle=None, length=None):
        if p is None:
            p = self.a
        if angle is None:
            angle = self.angle
        if length is None:
            length = self.length

        return cart_to_polar(p, angle, length)

    def set_angle(self, angle=None):
        if angle:
            self.angle = angle
        self.b.setp(self.cart_to_polar())

    def render(self, s):
        r = (self.id * 50) % 255
        color = (r, 100, 0)
        pg.draw.line(s, color, self.a.int(), self.b.int())
        pg.draw.circle(s, (255, 0, 0), self.a.int(), 5)
        pg.draw.circle(s, (0, 0, 255), self.b.int(), 5)

    def __repr__(self):
        return f'<{self.a}, {self.b}>'

    def __str__(self):
        return self.__repr__()
