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
        self.constraint = Constraint()

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

    def to_axis(self):
        # Turn this limb pos into a 1 demensional
        # between [0-1]
        rel_angle = self.angle
        if self.parent:
            rel_angle -= self.parent.angle
        return self.constraint.to_axis(rel_angle)

    def from_axis(self, axis):
        # Go from that axis defined above back to normal
        rel_angle = self.constraint.from_axis(axis)
        if self.parent:
            rel_angle += self.parent.angle
        self.set_angle(rel_angle)
        return rel_angle

    def add_constraint(self, _min=None, _max=None):
        if _min:
            self.constraint.min = _min
        if _max:
            self.constraint.max = _max

    def render(self, s):
        self.render_seg(s)
        self.render_const(s)

    def render_seg(self, s):
        r = (self.id * 50) % 255
        color = (r, 100, 0)
        pg.draw.line(s, color, self.a.int(), self.b.int(), 10)
        pg.draw.circle(s, (255, 0, 0), self.a.int(), 10)
        pg.draw.circle(s, (0, 0, 255), self.b.int(), 10)

    def render_const(self, s):
        _min = self.constraint.min
        _max = self.constraint.max

        if _min == 0 and _max == math.pi * 2:
            return

        if self.parent:
            _min += self.parent.angle
        _max += _min 

        min_point = self.cart_to_polar(self.a, _min, 30)
        min_color = (50, 50, 100)
        pg.draw.line(s, min_color, self.a.int(), min_point.int(), 5)

        max_point = self.cart_to_polar(self.a, _max, 30)
        max_color = (100, 50, 50)
        pg.draw.line(s, max_color, self.a.int(), max_point.int(), 5)

    def __repr__(self):
        return f'<{self.a}, {self.b}>'

    def __str__(self):
        return self.__repr__()


class Constraint():

    def __init__(self, _min=0, _max=None):
        _max = _max if _max else math.pi * 2
        self.min = _min
        self.max = _max

    def to_axis(self, angle):
        angle %= math.pi * 2
        angle -= self.min
        angle /= self.max
        return angle

    def from_axis(self, axis):
        angle = axis
        angle *= self.max
        angle += self.min
        return angle
