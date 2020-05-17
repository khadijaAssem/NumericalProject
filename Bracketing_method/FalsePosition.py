import timeit
import numpy
import sympy
import matplotlib.pyplot as plt

class FP:
    def __init__(self, fn, xl, xu, max_iterations, epsilon):
        self.iterations = []
        self.ea = 0
        self.xr = 0
        self.xr_prev = 0
        self.xl = xl
        self.xu = xu
        self.xr_value = 0
        self.xr_prev_value = 0
        self.xl_value = 0
        self.xu_value = 0
        self.number_of_iterations = 0
        self.fn = fn
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
            self.xl_value, self.xu_value = value_eqn(self.xl), value_eqn(self.xu)
            if self.xl_value * self.xu_value > 0:
                raise ValueError("Pitfall , can't find a root using bisection method")
            self.xr = (self.xl*self.xu_value - self.xu*self.xl_value) / (self.xu_value - self.xl_value)
            self.xr_value = value_eqn(self.xr)
            self.ea = abs((self.xr - self.xr_prev) / self.xr) * 100
            iteration = numpy.array((self.xl, self.xu, self.xr, self.ea),
                                    dtype=[('xl', numpy.float), ('xu', numpy.float), ('xr', numpy.float),
                                           ('err', numpy.float)])
            self.iterations.append(iteration)
            self.number_of_iterations += 1
            if self.xr_value * self.xl_value < 0:
                self.xu = self.xr
            elif self.xr_value * self.xl_value > 0:
                self.xl = self.xr
            else:
                break
            self.xr_prev = self.xr


            if self.ea < self.epsilon or self.number_of_iterations > self.max_iterations :
                break

        execution_time = timeit.default_timer() - start_time

        return self.number_of_iterations, execution_time, self.iterations, self.xr, self.ea , value_eqn

    def draw_plot(self, iterations, function):
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

        plt.plot(xpts, function(xpts), label='f\'(x)', color='b')
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.plot([xl, xl], [0, function(xl)], color='y', label='xl')
        plt.plot([xr, xr], [0, function(xr)], color='r', label='xr')
        plt.plot([xu, xu], [0, function(xu)], color='y', label='xu')
        plt.legend()
        plt.show()

x = sympy.Symbol('x')
obj = FP(x**3 - 2*x**2 + 1, -1, 0, 0, 0)
Result = obj.solve()
print(Result[0])
print(Result[1])
print(*Result[2], sep=", ")
print(Result[3])
print(Result[4])