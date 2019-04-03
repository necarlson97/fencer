from itertools import combinations_with_replacement


class Solver():

    # Determines how much we tweak each axis
    step_size = 0.05

    # Given a list of inputs, and 
    # a way of evaluating those inputs,
    # tweak the settings to minimize that evaluatior
    # TODO maybe we should normalize first, so
    # step size is actually meaningful
    @staticmethod
    def choose_setting(settings, evaluator):
        # NOTE: could do quadratic, but this
        # is just trying 1 axis at a time

        # It is possible that doing no tweak is the best
        ss = Solver.step_size
        tweaks = [-ss, 0, ss]

        # Try an array of tweak settings
        def try_tweaks(tweak_settings):
            sets = [s for s in settings]
            for i in range(len(sets)):
                sets[i] += tweak_settings[i]
            return evaluator(sets)

        all_combos = combinations_with_replacement(tweaks, len(settings))

        # Find best tweak settings
        best_tweaks = min(all_combos, key=try_tweaks)
        # Set best tweaks
        for i in range(len(settings)):
            settings[i] += best_tweaks[i]

        return settings
