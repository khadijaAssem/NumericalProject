import timeit
import numpy
import sympy
from sympy.abc import x
import matplotlib.pyplot as plt


def solve(equation, xl, xu, max_iterations=50, epsilon=0.0001):
    number_iterations = 0
    start_time = timeit.default_timer()
    try:
        simple_fun = sympy.simplify(equation)
        #print(simple_fun)
        symbol = simple_fun.free_symbols.pop()
        #print(symbol)
        function = sympy.lambdify(symbol, simple_fun)
    except ValueError:
        raise ValueError("Not a valid function")

    xr = 0
    xr_prev = 0
    error = 100
    iterations = []
    while True:
        xl_value, xu_value = function(xl), function(xu)
        if xl_value * xu_value > 0:
            raise ValueError("Pitfall , can't find a root using bisection method")
        xr = (xl + xu) / 2
        xr_value = function(xr)

        iteration = numpy.array((xl, xu, xr, error),
                                dtype=[('xl', numpy.float), ('xu', numpy.float), ('xr', numpy.float),
                                       ('err', numpy.float)])
        error = abs((xr - xr_prev) / xr) * 100
        iterations.append(iteration)
        if xr_value * xl_value < 0:
            xu = xr
        elif xr_value * xl_value > 0:
            xl = xr
        else:
            break
        xr_prev = xr
        number_iterations += 1
        if abs(xu - xl) < epsilon or number_iterations > max_iterations:
            break

    execution_time = timeit.default_timer() - start_time


    return number_iterations, execution_time, iterations, xr, error, function

def draw_plot(iterations, function):
    iteration = iterations[0]
    xl = iteration['xl']
    xu = iteration['xu']
    xr = iteration['xr']

    diff = xu - xl
    start = xl - 0.5 * diff
    end = xu + 0.5 * diff
    if diff == 0:
        start = -10
        end = 10
    xpts = numpy.linspace(start, end, 100)
    OX = 0 * xpts
    # x = np.linspace(-1,2)             # define the mesh in (-1,2)
    # OX = 0*x

    plt.plot(xpts, function(xpts),label='f(x)',color ='b')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.plot([xl, xl], [0, function(xl)], color='y', label='xl')
    plt.plot([xr, xr], [0, function(xr)], color='r', label='xr')
    plt.plot([xu, xu], [0, function(xu)], color='y', label='xu')
    plt.legend()
    plt.show()


number_iterations, execution_time, iterations, xr, error, function = solve(x**3 - 2*x**2 + 1,-1, 0, 50, 0.0001)
draw_plot(iterations, function)
