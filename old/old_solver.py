import numpy as np


class Solver():

    # Determines how quickly we move twoards solution
    learning_rate = 1
    # Determines when we stop (close enough)
    precision = 0.001

    # Soltion is multidimensional (iterator)
    last_step = None

    # Gradient descent solver to evaluate
    # possible kinematic moves, and choose best
    @staticmethod
    def choose_step(steps, dist_func):

        best_step = min(steps, key=dist_func)
        best_dist = dist_func(best_step)

        last_step = Solver.last_step
        Solver.last_step = best_step
        if last_step is None:
            return best_step

        # For each dimension in the solution, find the gradient
        # and apply the learning rate
        last_dist = dist_func(last_step)
        inputs = [last_step, best_step]
        outputs = [last_dist, best_dist]
        solution = []
        for i in range(len(best_step)):
            # Get all of the x, y, z, etc from the inputs
            d_in = [inp[i] for inp in inputs]
            grad = np.gradient([d_in, outputs], axis=0)
            # We only care about the gradient of the most
            # recent step. Also flip pos/neg
            print('  ', grad)
            grad = -grad[0].tolist()[0]

            # Apply learning rate and precision limit
            move = grad * Solver.learning_rate
            if abs(move) < Solver.precision:
                move = 0

            print('  in/out', i, d_in, outputs, grad, move)
            solution.append(best_step[i] + move)

        # Apply learning rate and limit precision
        # only care about grad[1], the gradient at the most recent step
        Solver.last_step = solution
        return solution
