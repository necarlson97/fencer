from solver import Solver

curr = [500, 9]
end = [2, 0]


def dist_func(settings):
    sx, sy = settings
    ex, ey = end
    dist = abs(ex - sx) + abs(ex - ey)
    return dist


for i in range(10):
    curr = Solver.choose_setting(curr, dist_func)
    print(curr)

print('final', curr, end)
