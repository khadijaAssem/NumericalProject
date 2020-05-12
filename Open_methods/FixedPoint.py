import sympy
import numpy
import timeit


class FP:
    def __init__(self, gx, xi, max_iterations, epsilon):
        self.iterations = []
        self.ea = 0
        self.xr = 0
        self.number_of_iterations = 0
        self.xi = xi
        self.gx = gx
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
            eqn = sympy.simplify(self.gx)
        except ValueError:
            raise ValueError("Error! Invalid function.")

        if len(eqn.free_symbols) != 1:
            raise ValueError("Error! Invalid function.")
        X = eqn.free_symbols.pop()

        try:
            value_eqn = sympy.lambdify(X, eqn)
        except ValueError:
            raise ValueError("Error! Invalid function.")

        count = 0

        while True:
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
                if count == 5:
                    raise ValueError("Oops! Error increase. So, it will diverge.")
            if self.ea < self.epsilon or self.number_of_iterations > self.max_iterations:
                break

        execution_time = timeit.default_timer() - start_time

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea


x = sympy.Symbol('x')
obj = FP((x ** 2 - 3) / 2, 4, None, None)

Result = obj.solve()
print(Result[0])
print(Result[1])
print(*Result[2], sep=", ")
print(Result[3])
print(Result[4])
