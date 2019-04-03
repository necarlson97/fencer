import math

import pygame as pg

from point import Point
from segment import Segment, cart_to_polar
from solver import Solver


# TODO DONT HARDCODE
width, height = (1000, 800)


class Limb():

    def __init__(self, root=None):
        self.root = root if root else Point()
        self.target = Point()
        self.segments = []

        self.pinned = True

    def add_segment(self, segment):
        if not self.segments:
            segment.a = self.root
        self.segments.append(segment)
        segment.set_angle()

    def update(self):
        # Update target to mouse position
        # m_pos = pg.mouse.get_pos()
        # self.target.set(*m_pos)

        self.target.set(500, 300)

        axes = self.get_axes()
        curried_eval = self.create_follow_eval()

        new_axes = Solver.choose_setting(axes, curried_eval)
        self.update_segments(new_axes)

        # print(new_axes)
        # print([s.angle for s in self.segments])
        # print([s.length for s in self.segments])

    def update_segments(self, axes=None):
        root, angles = self.convert_axes(axes)
        self.root.setp(root)

        for i in range(len(self.segments)):
            seg = self.segments[i]
            a = angles[i] if angles else None
            seg.set_angle(a)

    def render(self, s):
        self.render_target(s)
        for seg in self.segments:
            seg.render(s)

    def render_target(self, s):
        curr_score = self.create_follow_eval()(self.get_axes())
        pg.draw.circle(s, (255, 255, 255), self.target.int(), 10)
        color = (0, (1 - curr_score) * 100, 0)
        pg.draw.circle(s, color, self.target.int(), 20, 5)

    def get_axes(self):
        # Can move the angles to aproach target
        # (and normalize)
        def norm_ang(a):
            return (a / (math.pi * 2)) % 1
        axes = [norm_ang(s.angle) for s in self.segments]
        # Can move the root (if it is not pinned)
        if not self.pinned:
            axes += [self.root.x / width, self.root.y / height]
        return axes

    def convert_axes(self, axes):
        if axes is None:
            return self.root, None

        # un-normalize
        if not self.pinned:
            ry = axes[-1] * height
            rx = axes[-2] * width
            angles = [a * 2 * math.pi for a in axes[:-2]]
            return Point(rx, ry), angles
        else:
            return self.root, [a * 2 * math.pi for a in axes]

    def create_follow_eval(self):

        def evaluator(axes):
            # Evaluate how far this limbs end is
            # from the target end

            root, angles = self.convert_axes(axes)

            p = root
            for i in range(len(angles)):
                a = angles[i]
                length = self.segments[i].length
                p = cart_to_polar(p, a, length)

            dist = p.distp(self.target)
            # We normalize distance by the maximum,
            # which is the diagonal
            max_dist = math.sqrt(width**2 + height**2)
            return dist / max_dist

        return evaluator


def create_arm(x=500, y=500):
    root = Point(x, y)
    limb = Limb(root)

    bicep = Segment(length=200)
    fore = Segment(bicep, length=180)
    hand = Segment(fore, length=50)

    limb.add_segment(bicep)
    limb.add_segment(fore)
    limb.add_segment(hand)

    return limb
