import math
import random as rand
from itertools import combinations_with_replacement


class Solver():

    precision = 0.05

    @staticmethod
    def choose_setting(settings, evaluator):
        # nieve quadratic
        step_count = int(1 / Solver.precision)
        print(step_count)
        all_steps = [i * Solver.precision
                     for i in range(step_count)]
        all_settings = combinations_with_replacement(all_steps, len(settings))

        best_settings = min(all_settings, key=evaluator)

        return best_settings
