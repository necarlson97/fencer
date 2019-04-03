import math
import random as rand


class Solver():

    # Determines how much we can tweak each axis
    max_step_size = 0.1
    step_size = max_step_size
    min_step_size = 0.001
    # For each run, how many rand settings do we try?
    step_iters = 50
    # Determines when is good enough
    precision = 0.001

    def random_step():
        r = rand.random() * Solver.step_size * 2
        r -= Solver.step_size
        return r

    def dec_step_size():
        Solver.step_size -= 0.1
        Solver.step_size = max(Solver.min_step_size, Solver.step_size)

    def inc_step_size():
        Solver.step_size *= 2
        Solver.step_size = min(Solver.max_step_size, Solver.step_size)

    @staticmethod
    def choose_setting(settings, evaluator):

        def create_rand_setting():
            return [s + Solver.random_step()
                    for s in settings]

        rand_steps = [create_rand_setting()
                      for i in range(Solver.step_iters)]

        best_settings = min(rand_steps, key=evaluator)

        score = evaluator(best_settings)
        if score < 0.01:
            Solver.dec_step_size()
        else:
            Solver.inc_step_size()

        Solver.last_score = score
        return best_settings
