import sympy
import numpy
import math
import timeit
import matplotlib.pyplot as plt


class NR:
    def __init__(self, fn, xi, max_iterations, epsilon):
        self.iterations = []
        self.ea = 0
        self.xr = 0
        self.number_of_iterations = 0
        self.xi = xi
        self.fn = fn
        if max_iterations is None:
            self.max_iterations = 50
        else:
            self.max_iterations = max_iterations
        if epsilon is None:
            self.epsilon = 0.0001
        else:
            self.epsilon = epsilon

    def solve(self):
        start_time = timeit.default_timer()

        try:
            eqn = sympy.simplify(self.fn)
        except ValueError:
            raise ValueError("Error! Invalid function.")

        if len(eqn.free_symbols) != 1:
            raise ValueError("Error! Invalid function.")
        X = eqn.free_symbols.pop()

        try:
            diff = sympy.diff(eqn, X)
            value_eqn = sympy.lambdify(X, eqn)
            value_diff = sympy.lambdify(X, diff)
        except ValueError:
            raise ValueError("Error! Invalid function.")

        while True:
            if value_diff(self.xi) == 0:
                raise ValueError("Oops! Pitfall,Division by Zero.")
            self.xr = self.xi - (value_eqn(self.xi) / value_diff(self.xi))
            self.ea = abs((self.xr - self.xi) / self.xr) * 100
            iteration = numpy.array((self.xi, self.xr, self.ea),
                                    dtype=[('current_approximate', numpy.float),
                                           ('approximate_root', numpy.float),
                                           ('error', numpy.float)])
            self.iterations.append(iteration)
            self.xi = self.xr
            self.number_of_iterations += 1

            if self.ea < self.epsilon or self.number_of_iterations > self.max_iterations or value_eqn(self.xi) == 0:
                break

        execution_time = timeit.default_timer() - start_time

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea, value_eqn

    def draw_plot(iterations, function):
        iteration = iterations[0]
        xi = iteration['current_approximate']
        xr = iteration['approximate_root']
        diff = max(xi, xr) - min(xi, xr)
        start = min(xi, xr) - 0.25 * 10*diff
        end = max(xi, xr) + 0.25 * 10*diff
        if diff == 0:
            start = -10
            end = 10
        xpts = numpy.linspace(start, end, 100)
        OX = 0 * xpts
        # x = np.linspace(-1,2)             # define the mesh in (-1,2)
        # OX = 0*x

        plt.plot(xpts, function(xpts), label='f(x)', color='b')
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.plot([xi, xi], [0, function(xi)], color='y', label='Xi')
        plt.plot([xr, xr], [0, function(xr)], color='r', label='Xi+1')
        plt.legend()
        plt.show()


x = sympy.Symbol('x')
obj = NR(0.95*x**3-5.9*x**2+10.9*x-6, 3.5, None, None)
number_of_iterations, execution_time, iterations, xr, ea, value_eqn = obj.solve()
#Result = obj.solve()
#print(Result[0])
#print(Result[1])
#print(*Result[2], sep=", ")
#print(Result[3])
#print(Result[4])
#print(Result[5])

#0.95*x**3-5.9*x**2+10.9*x-6, 3.5

NR.draw_plot(iterations, value_eqn)