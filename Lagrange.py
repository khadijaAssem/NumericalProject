import numpy as np

# import matplotlib.pyplot as plt

from numpy.polynomial import Polynomial as P


class Lagrange:
    X = []
    Y = []
    coff = []
    No = []
    m = 0

    def __init__(self, X, Y, t):
        self.X = X
        self.Y = Y
        self.t = t
        self.m = len(X)

    def lagrange(self):
        for i in range(len(self.X)):
            self.X[i] = float(self.X[i])
            self.Y[i] = float(self.Y[i])
        t = float(self.t)
        for i in range(self.m):
            no = 1
            temp = []
            for j in range(self.m):
                if i != j:
                    no *= (self.X[i] - self.X[j])
                    temp.append(self.X[j])
            self.No.append(self.Y[i] * 1 / no)
            self.coff.append(temp)

    def calc_value(self, c):
        res = 0
        for i in range(self.m):
            no = 1
            for j in range(self.m):
                if i != j:
                    no *= (c - self.X[j]) / (self.X[i] - self.X[j])
            res += self.Y[i] * no
        return res

    def poly(self):
        poly = ""
        for i in range(self.m):
            if self.Y[i] != 0:
                poly += str(self.No[i])
            for j in range(self.m - 1):
                if self.coff[i][j] > 0:
                    poly += "(x-" + str(self.coff[i][j]) + ")"
                else:
                    poly += "(x+" + str(-1 * self.coff[i][j]) + ")"

            if i != self.m - 1:
                poly += " + "
        return poly

    def plot(self):
        step = (self.X[0] - self.X[len(self.X) - 1]) / 10000
        values_x = []
        values_y = []
        for i in range(10000 + 3):
            values_y.append(self.calc_value(self.X[0] + step * i))
            values_x.append(self.X[0] + step * i)
        plt.plot(values_x, values_y)
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("graph!")
        plt.show()