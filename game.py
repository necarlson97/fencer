import pygame as pg
from limb import create_arm


class Game():

    bg = (0, 0, 0)
    dev = False

    def __init__(self, display):
        self.display = display

        self.input_objects = []
        self.update_objects = [create_arm()]
        self.render_objects = self.update_objects

    def inputs(self, events):
        for e in [e for e in events if e.type == pg.KEYDOWN]:
            k = e.key
            print('Key pressed:', k)

            # one = dev mode
            if k == 49:
                Game.dev = not Game.dev

            # space = ?
            if k == 32:
                pass

            # right = ?, left = ?
            if k == 275:
                pass
            if k == 276:
                pass

        for io in self.input_objects:
            io.inputs(events)

    def update(self):
        for o in self.update_objects:
            o.update()

    def render(self, s):
        s.fill(self.bg)

        for o in self.render_objects:
            o.render(s)
        if Game.dev:
            for o in self.render_objects:
                if not hasattr(o, 'post_render'):
                    continue
                o.post_render(s)
