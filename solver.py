import math
import random as rand


class Solver():

    # Determines how much we tweak each axis
    step_size = 0.01
    # Determines when is good enough
    precision = 0.0000001

    # Given a list of inputs, and 
    # a way of evaluating those inputs,
    # tweak the settings to minimize that evaluatior
    prev_settings = [None, None]
    prev_scores = [1, 1]

    @staticmethod
    def choose_setting(settings, evaluator):
        # NOTE: could do quadratic, but this
        # is just trying 1 axis at a time

        for i in range(len(settings)):
            grad = Solver.calc_grad(i)
            step = grad * Solver.step_size

            if abs(step) > Solver.precision:
                settings[i] -= step

        score = evaluator(settings)

        # update scores
        Solver.prev_scores[0] = Solver.prev_scores[1]
        Solver.prev_scores[1] = score

        # update settings
        Solver.prev_settings[0] = Solver.prev_settings[1]
        Solver.prev_settings[1] = settings

        return settings

    def calc_grad(i):
        p_scores = Solver.prev_scores
        p_settings = Solver.prev_settings

        d_score = p_scores[1] - p_scores[0]
        if Solver.prev_settings[0]:
            d_setting = p_settings[1][i] - p_settings[0][i]
        else:
            d_setting = rand.random() - 0.5

        # no need to update if there is no difference
        if d_setting == 0:
            return 1

        clamped_d_setting = abs(d_setting) / d_setting
        grad = d_score * clamped_d_setting

        # print(p_scores, d_score, p_settings, d_setting, grad)
        return grad
