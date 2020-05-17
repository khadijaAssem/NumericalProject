from tkinter import messagebox

import sympy
import numpy
import timeit
import math
import matplotlib.pyplot as plt


class FP:
    def __init__(self, gx, xi, max_iterations, epsilon):
        self.iterations = []
        self.ea = float(0)
        self.xr = float(0)
        self.number_of_iterations = 0
        self.xi = float(xi)
        self.gx = gx
        if max_iterations == 0:
            self.max_iterations = 50
        else:
            self.max_iterations = max_iterations
        if epsilon == 0:
            self.epsilon = 0.0001
        else:
            self.epsilon = epsilon

    def solve(self):
        start_time = timeit.default_timer()

        try:
            eqn = sympy.simplify(self.gx)
            if len(eqn.free_symbols) != 1:
                messagebox.showerror("Oops!", "Error! Invalid function.")
                raise ValueError("Error! Invalid function.")
            X = eqn.free_symbols.pop()
        except ValueError:
            messagebox.showerror("Oops!", "Error! Invalid function.")
            raise ValueError("Error! Invalid function.")

        try:
            diff = sympy.diff(eqn, X)
            value_eqn = sympy.lambdify(X, eqn)
            value_diff = sympy.lambdify(X, diff)
        except ValueError:
            messagebox.showerror("Oops!", "Error! Invalid function.")
            raise ValueError("Error! Invalid function.")

        count = 0
        first = True

        while True:
            if first and value_diff(self.xi) > 1:
                first = False
                messagebox.showerror("Oops!", "Error increases. So, it will diverge.")
                raise ValueError("Oops! Error increases. So, it will diverge.")
            self.xr = value_eqn(self.xi)
            ea_prev = self.ea
            self.ea = abs((self.xr - self.xi) / self.xr) * 100

            iteration = numpy.array((self.xi, self.xr, self.ea),
                                    dtype=[('current_approximate', numpy.float),
                                           ('approximate_root', numpy.float),
                                           ('error', numpy.float)])
            self.iterations.append(iteration)
            self.xi = self.xr
            self.number_of_iterations += 1

            if ea_prev < self.ea:
                count += 1
            if self.ea < self.epsilon or self.number_of_iterations > self.max_iterations:
                break

        execution_time = timeit.default_timer() - start_time

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea , value_eqn

    def draw_plot(self, iterations, value_eqn):
        iteration = iterations[0]
        xi = iteration['current_approximate']
        xr = iteration['approximate_root']
        diff = max(xi, xr) - min(xi, xr)
        start = min(xi, xr) - 0.25 * 10 * diff
        end = max(xi, xr) + 0.25 * 10 * diff
        if diff == 0:
            start = -10
            end = 10
        xpts = numpy.linspace(start, end, 100)

        plt.plot(xpts, value_eqn(xpts), label='g(x)', color='b')
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.plot([xi, xi], [0, value_eqn(xi)], color='y', label='Xi')
        plt.plot([xr, xr], [0, value_eqn(xr)], color='r', label='Xi+1')
        plt.legend()
        plt.show()


x = sympy.Symbol('x')
# obj = FP(((2*x+3)**(1/2)), 4, 0, 0)
# obj = FP((3/(x-2)), 4, 0, 0)
obj = FP((1 + (1/x)), 2, 0, 0)

Result = obj.solve()
print(Result[0])
print(Result[1])
print(*Result[2], sep=", ")
print(Result[3])
print(Result[4])


