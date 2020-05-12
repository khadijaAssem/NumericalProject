import sympy
import numpy
import timeit


class SC:
    def __init__(self, fn, x_prev, xi, max_iterations, epsilon):
        self.iterations = []
        self.ea = 0
        self.xr = 0
        self.number_of_iterations = 0
        self.x_prev = x_prev
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
            value_eqn = sympy.lambdify(X, eqn)
        except ValueError:
            raise ValueError("Error! Invalid function.")

        while True:
            if value_eqn(self.x_prev) - value_eqn(self.xi) == 0:
                raise ValueError("Oops! Pitfall,Division by Zero.")

            self.xr = self.xi - ((value_eqn(self.xi)*(self.x_prev-self.xi)) / (value_eqn(self.x_prev) - value_eqn(self.xi)))
            self.ea = abs((self.xr - self.xi) / self.xr) * 100
            iteration = numpy.array((self.x_prev, self.xi, self.xr, self.ea),
                                    dtype=[('previous_approximate', numpy.float)
                                        , ('current_approximate', numpy.float)
                                        , ('approximate_root', numpy.float),
                                           ('error', numpy.float)])
            self.iterations.append(iteration)
            self.x_prev = self.xi
            self.xi = self.xr
            self.number_of_iterations += 1

            if self.ea < self.epsilon or self.number_of_iterations > self.max_iterations:
                break

        execution_time = timeit.default_timer() - start_time

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea


x = sympy.Symbol('x')
obj = SC((sympy.cos(x) + 2*sympy.sin(x) + x**2), 0, -0.1, 100, 0.001)

Result = obj.solve()
print(Result[0])
print(Result[1])
print(*Result[2], sep=", ")
print(Result[3])
print(Result[4])
