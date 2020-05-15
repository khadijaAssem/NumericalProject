import timeit
import numpy
import sympy
from sympy.abc import x
import matplotlib.pyplot as plt


def solve(equation, approx_root, max_iterations=50, epsilon=0.0001):
    number_iterations = 0
    start_time = timeit.default_timer()
    try:
        simple_fun = sympy.simplify(equation)
        print(simple_fun)
        symbol = simple_fun.free_symbols.pop()
        print(symbol)

        simple_fun = sympy.Add(symbol, simple_fun)
        print(simple_fun)
        function = sympy.lambdify(symbol, simple_fun)
    except ValueError:
        raise ValueError("Not a valid function")

    prev_app=approx_root
    error = 100
    iterations = []
    while True:
        approx_root = function(prev_app)
        error = abs((approx_root - prev_app) / approx_root) * 100
        iteration = numpy.array((prev_app, approx_root, error),
                                dtype=[('prev_app', numpy.float), ('approx_root', numpy.float),
                                       ('err', numpy.float)])
        iterations.append(iteration)
        prev_app=approx_root
        number_iterations += 1
        if error < epsilon or number_iterations > max_iterations:
            break

    execution_time = timeit.default_timer() - start_time


    return number_iterations, execution_time, iterations, approx_root, error, function
number_iterations, execution_time, iterations, approx_root, error, function = solve(x**2-x, -1, 50, 0.0001)
print(approx_root)
