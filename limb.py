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

    def add_segment(self, segment):
        if not self.segments:
            segment.a = self.root
        self.segments.append(segment)
        segment.set_angle()

    def update(self):
        # Update target to mouse position
        m_pos = pg.mouse.get_pos()
        self.target.set(*m_pos)

        # self.target.set(500, 300)

        axes = self.get_axes()
        curried_eval = self.create_follow_eval()

        new_axes = Solver.choose_setting(axes, curried_eval)
        self.convert_axes(new_axes)

        # print(new_axes)
        # print([s.angle for s in self.segments])
        # print([s.length for s in self.segments])

    # def update_segments(self, axes=None):
    #     root, angles = self.convert_axes(axes)
    #     self.root.setp(root)

    #     for i in range(len(self.segments)):
    #         seg = self.segments[i]
    #         a = angles[i] if angles else None
    #         seg.set_angle(a)

    def render(self, s):
        self.render_target(s)
        for seg in self.segments:
            seg.render(s)

    def render_target(self, s):
        curr_score = self.create_follow_eval()(self.get_axes())
        print(curr_score)
        pg.draw.circle(s, (255, 255, 255), self.target.int(), 10)
        r = curr_score * 255
        color = (r, 0, 0)
        pg.draw.circle(s, color, self.target.int(), 20, 5)

    def get_axes(self):
        # Can move the angles to aproach target
        # (and normalize)

        # We are only concerned with bicept and forearm,
        # wrist is NOT a part of IK
        
        axes = [s.to_axis() for s in self.segments[:-1]]
        return axes

    def convert_axes(self, axes):
        if axes is None:
            return self.root, None

        # Because wrist is not controlled by IK,
        # we leave it alone
        angles = []
        for i in range(len(axes)):
            axis = axes[i]
            seg = self.segments[i]
            angles.append(seg.from_axis(axis))

        # We leave wrist as is, but still update it visually
        wrist = self.segments[-1]
        angles += [wrist.angle]
        wrist.set_angle()
        return self.root, angles

    def create_follow_eval(self):

        # The most important part of the evaluator,
        # telling if the wrist is at the correct position
        def score_position(root, angles):
            p = root
            for i in range(len(angles) - 1):
                a = angles[i]
                length = self.segments[i].length
                p = cart_to_polar(p, a, length)

            dist = p.distp(self.target)
            # We normalize distance by the maximum,
            # which is the diagonal
            max_dist = math.sqrt(width**2 + height**2)
            return dist / max_dist

        # The second most important part,
        # telling that the bicept is relaxed
        # TODO could just make this a constraint
        def score_comfort(root, angles):
            bicept_ang = angles[0]
            score = (bicept_ang - math.pi) / math.pi
            if score < 0:
                return 0
            return score

        def evaluator(axes):
            # Evaluate how far this limbs end is
            # from the target end

            root, angles = self.convert_axes(axes)

            pos_score_weight = 1
            pos_score = score_position(root, angles)
            return pos_score

        return evaluator


def create_arm(x=500, y=400):
    root = Point(x, y)
    limb = Limb(root)

    bicep = Segment(length=200)
    fore = Segment(bicep, length=180)
    hand = Segment(fore, length=50)

    bicep.add_constraint(-math.pi/2, math.pi)
    fore.add_constraint(math.pi, math.pi)

    limb.add_segment(bicep)
    limb.add_segment(fore)
    limb.add_segment(hand)

    return limb
