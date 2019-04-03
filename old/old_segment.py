import math

import pygame as pg

from point import Point


class Segment():

    count = 0

    # a is the root
    # b is the tip

    def __init__(self, parent=None, length=20, angle=0):
        self.a = Point()
        self.angle = angle
        self.length = length

        if parent:
            self.b = parent.a.copy()
            self.parent = parent
        else:
            self.b = Point()
            self.parent = None

        self.id = Segment.count
        Segment.count += 1

        self.pinned = False

    def cart_to_polar(self, p=None, angle=None, length=None):
        if p is None:
            p = self.a
        if angle is None:
            angle = self.angle
        if length is None:
            length = self.length

        polx = length * math.cos(angle)
        poly = length * math.sin(angle)
        r = Point(polx, poly).add(p)
        return r

    def diff_angle(self, p):
        # Define some points
        p1 = self.a
        p2 = self.b
        p3 = p

        at1 = math.atan2(p3.y - p1.y, p3.x - p1.x)
        at2 = math.atan2(p2.y - p1.y, p2.x - p1.x)
        return at1 - at2

    def follow(self, p=None):
        # target to follor
        if p is None:
            p = self.parent.a

        self.angle += self.diff_angle(p)
        self.a = self.cart_to_polar(p, self.angle, -self.length)

    def update(self):

        if not self.pinned:
            mp = Point(*pg.mouse.get_pos())
            target = mp if not self.parent else None
            self.follow(target)
        self.b = self.cart_to_polar()

    def render(self, s):
        r = (self.id * 10) % 255
        color = (r, 100, 0)
        pg.draw.line(s, color, self.a.int(), self.b.int())
        pg.draw.circle(s, (255, 0, 0), self.a.int(), 5)
        pg.draw.circle(s, (0, 0, 255), self.b.int(), 5)

    def __repr__(self):
        return f'<{self.a}, {self.b}>'

    def __str__(self):
        return self.__repr__()


def create_segments(n=10):

    segs = []
    parent = None
    for i in range(n):
        seg = Segment(parent)
        parent = seg
        segs.append(seg)
    segs[-1].a.set(500, 500)
    segs[-1].pinned = True
    return segs
