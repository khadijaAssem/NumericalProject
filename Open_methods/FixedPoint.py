import sympy
import numpy
import timeit
import math

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

        count = 0
        first = True

        while True:
            if first and value_diff(self.xi) > 1:
                first = False
                raise ValueError("Oops! Error increase. So, it will diverge.")
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

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea


x = sympy.Symbol('x')
#obj = FP(((2*x+3)**(1/2)), 4, 0, 0)
#obj = FP((3/(x-2)), 4, 0, 0)
obj = FP(((x**2-3)/2), 4, 0, 0)

Result = obj.solve()
print(Result[0])
print(Result[1])
print(*Result[2], sep=", ")
print(Result[3])
print(Result[4])