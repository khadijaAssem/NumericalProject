from tkinter import *
from tkinter import ttk, filedialog
import numpy as np
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Open_methods import FixedPoint, NewtonRaphson, Secant
import Lagrange
import Newton


class GUI:
    master = None
    part1 = None
    part2 = None
    polynomiaOrder = None

    def __init__(self, master):
        self.v = IntVar()
        self.master = master
        master.title("Numerical Project")
        master.geometry('570x500')
        self.createTabs()
        self.buildPart1()
        self.buildPart2()

    def createTabs(self):
        tabControl = ttk.Notebook(self.master)
        self.part1 = ttk.Frame(tabControl)
        self.part2 = ttk.Frame(tabControl)
        tabControl.add(self.part1, text='Part 1')
        tabControl.add(self.part2, text='Part 2')
        tabControl.pack(expand=1, fill="both")

    def buildPart2(self):
        polyOrderLabel = Label(self.part2, text="Enter the polynomial Order").grid(column=0, row=0, padx=10, pady=10)
        self.polyOrderEntry = Entry(self.part2, width=10)
        self.polyOrderEntry.grid(column=1, row=0, padx=10, pady=10)
        self.polyOrderEntry.bind("<Return>", self.readInput)
        orLabel = Label(self.part2, text="Or").grid(column=3, row=0, padx=10, pady=10)
        read_button = Button(self.part2, width=20, height=1, text="Read data from file",
                             command=self.readFromFile).grid(row=0, column=4)

    def buildPart1(self):
        MODES = [
            ("Bisection", 1),
            ("False Position", 2),
            ("Fixed Point", 3),
            ("Newton Raphson", 4),
            ("Secant", 5),
        ]
        i = 0
        self.v.set(4)
        for text, mode in MODES:
            b = Radiobutton(self.part1, text=text,
                            variable=self.v, value=mode, indicatoron=False,
                            command=lambda: GUI.clicked(self, self.v.get())).grid(column=i, row=0, padx=10, pady=10)
            i += 1

    def clicked(self, value):
        fxlabel = Label(self.part1, text="F(x)")
        gxlabel = Label(self.part1, text="g(x)")
        xilabel = Label(self.part1, text="Initial Approximation")
        xprevlabel = Label(self.part1, text="Previous Approximation")
        iterlabel = Label(self.part1, text="max iterations")
        epsilonlabel = Label(self.part1, text="epsilon")

        self.fEntry = Entry(self.part1, width=30)
        self.xiEntry = Entry(self.part1, width=30)
        self.xprevEntry = Entry(self.part1, width=30)
        self.iterEntry = Entry(self.part1, width=30)
        self.epsilonEntry = Entry(self.part1, width=30)

        button = Button(self.part1, width=10, height=1, text="Solve", command=self.solveP2)
        button.grid(column=2, row=7, padx=20, pady=20)

        xprevlabel.grid(column=0, row=3, padx=10, pady=10)
        xilabel.grid(column=0, row=4, padx=10, pady=10)
        iterlabel.grid(column=0, row=5, padx=10, pady=10)
        epsilonlabel.grid(column=0, row=6, padx=10, pady=10)

        self.fEntry.grid(column=1, row=2, padx=10, pady=10)
        self.xprevEntry.grid(column=1, row=3, padx=10, pady=10)
        self.xiEntry.grid(column=1, row=4, padx=10, pady=10)
        self.iterEntry.grid(column=1, row=5, padx=10, pady=10)
        self.epsilonEntry.grid(column=1, row=6, padx=10, pady=10)

        if self.v.get() == 1:
            print(1)
        elif self.v.get() == 2:
            print(2)
        elif self.v.get() == 3:
            fxlabel.config(DISABLED)
            self.xprevEntry.config(state='disabled')
            gxlabel.grid(column=0, row=2, padx=10, pady=10)
        elif self.v.get() == 4:
            gxlabel.config(DISABLED)
            self.xprevEntry.config(state='disabled')
            fxlabel.grid(column=0, row=2, padx=10, pady=10)
        elif self.v.get() == 5:
            gxlabel.config(DISABLED)
            self.xprevEntry.config(state='normal')
            fxlabel.grid(column=0, row=2, padx=10, pady=10)

    def readInput(self, entry):
        self.polynomiaOrder = int(entry.widget.get())
        columnLabel = 0;
        columnX = 1;
        columnY = 2
        row = 1
        self.entryX = [None] * (self.polynomiaOrder)
        self.entryY = [None] * (self.polynomiaOrder)
        for i in range(1, self.polynomiaOrder + 1):
            label = Label(self.part2, text=("Point number " + str(i))).grid(column=columnLabel, row=(row + i), padx=10,
                                                                            pady=10)
            self.entryX[i - 1] = Entry(self.part2, width=10)
            self.entryX[i - 1].grid(column=columnX, row=(row + i), padx=5, pady=5)

            self.entryY[i - 1] = Entry(self.part2, width=10)
            self.entryY[i - 1].grid(column=columnY, row=(row + i), padx=5, pady=5)

            if ((i != 0) and (i % 15 == 0)):
                columnLabel += 3;
                columnX += 3;
                columnY += 3
                row = 1 - i

        self.completePart2(columnY, row + self.polynomiaOrder + 1)

    def completePart2(self, column, row):
        solve_for_x = Label(self.part2, text="Find value for    ").grid(row=row, column=column - 2)
        self.solve_for_x_entry = Entry(self.part2, width=25)
        self.solve_for_x_entry.grid(column=column - 1, row=row, padx=5, pady=5, columnspan=2)

        self.var = IntVar()
        R1 = Radiobutton(self.part2, text="newton", variable=self.var, value=1).grid(row=row + 1, column=column - 1)
        R2 = Radiobutton(self.part2, text="lagrange", variable=self.var, value=2).grid(row=row + 2, column=column - 1)

        solve_button = Button(self.part2, width=10, height=1, text="solve", command=self.solve).grid(column=column,
                                                                                                     row=row + 2,
                                                                                                     padx=10, pady=10)

    def readFromFile(self):
        X = []
        Y = []
        T = 0

        file_path = filedialog.askopenfilename()
        # read_from_file(file_path)

        f = open(file_path, "r")
        i = 0
        method = ""
        for x in f:
            if i == 0:
                method = str(x)
            elif i == 1:
                T = float(x)
            else:
                a = x.split(" ")
                X.append(float(a[0]))
                Y.append(float(a[1]))
            i += 1

        window = Toplevel(root)
        window.title("Solution")
        window.geometry('500x500')
        functionLabel = Label(window, text="Output function ").grid(row=0, column=1)
        solveLabel = Label(window, text=("Output at X = " + str(T))).grid(row=1, column=1)
        l = None
        n = None
        if method.__contains__("Lagrange"):

            l = Lagrange.Lagrange(X, Y, T)
            l.lagrange()
            outputLabel = Label(window, text=str(l.poly())).grid(row=0, column=3)
            solveOutput = Label(window, text=(str(l.calc_value(T)))).grid(row=1, column=3)

        elif method.__contains__("Newton"):
            n = Newton.Newton(X, Y, len(X))
            outputLabel = Label(window, text=str(n.createFormula())).grid(row=0, column=3)
            solveOutput = Label(window, text=(str(n.solve(T)))).grid(row=1, column=3)
        self.plot(X, l, n, method, window)

    def plot(self, X, l, n, method, window):

        values_y = []
        values_x = np.linspace(X[0], X[len(X) - 1], 10000)
        for i in range(len(values_x)):
            if method.__contains__("Lagrange"):
                values_y.append(l.calc_value(values_x[i]))
            else:
                values_y.append(n.solve(values_x[i]))
            # values_x.append(X[0] + step * i)
        fig = Figure()
        fig.add_subplot(111).plot(values_x, values_y)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=3)

    def solve(self):
        window = Toplevel(root)
        window.title("Newton")
        window.geometry('500x500')
        functionLabel = Label(window, text="Output function ").grid(row=0, column=1)
        solveLabel = Label(window, text=("Output at X = " + str(x))).grid(row=1, column=1)
        l = None
        n = None
        if self.var.get() == 2:
            method = "Lagrange"
            l = Lagrange.Lagrange(X, Y, x)
            l.lagrange()
            outputLabel = Label(window, text=str(l.poly())).grid(row=0, column=3)
            solveOutput = Label(window, text=(str(l.calc_value(x)))).grid(row=1, column=3)

        if self.var.get() == 1:
            method = "Newton"
            n = Newton.Newton(X, Y, self.polynomiaOrder)
            outputLabel = Label(window, text=str(n.createFormula())).grid(row=0, column=3)
            solveOutput = Label(window, text=(str(n.solve(x)))).grid(row=1, column=3)
        self.plot(X, l, n, method, window)

    def solveP2(self):
        window = Toplevel(root)
        window.title("Root Finder")
        window.geometry('500x500')
        iter = False
        eps = False
        if self.iterEntry.index("end") == 0:
            iter = True
        if self.epsilonEntry.index("end") == 0:
            eps = True
        if self.v.get() == 3:
            method = "Fixed Point"
            if iter and eps:
                F = FixedPoint.FP(self.fEntry, self.xiEntry, None, None)
            elif iter:
                F = FixedPoint.FP(self.fEntry, self.xiEntry, None, self.epsilonEntry)
            elif eps:
                F = FixedPoint.FP(self.fEntry, self.xiEntry, self.iterEntry, None)
            else:
                F = FixedPoint.FP(self.fEntry, self.xiEntry, self.iterEntry, self.epsilonEntry)
            F.solve()

        elif self.v.get() == 4:
            method = "Newton Raphson"
            if iter and eps:
                N = NewtonRaphson.NR(self.fEntry, self.xiEntry, None, None)
            elif iter:
                N = NewtonRaphson.NR(self.fEntry, self.xiEntry, None, self.epsilonEntry)
            elif eps:
                N = NewtonRaphson.NR(self.fEntry, self.xiEntry, self.iterEntry, None)
            else:
                N = NewtonRaphson.NR(self.fEntry, self.xiEntry, self.iterEntry, self.epsilonEntry)
            N.solve()

        elif self.v.get() == 5:
            method = "Secant"
            if iter and eps:
                S = Secant.SC(self.fEntry, self.xprevEntry, self.xiEntry, None, None)
            elif iter:
                S = Secant.SC(self.fEntry, self.xprevEntry, self.xiEntry, None, self.epsilonEntry)
            elif eps:
                S = Secant.SC(self.fEntry, self.xprevEntry, self.xiEntry, self.iterEntry, None)
            else:
                S = Secant.SC(self.fEntry, self.xprevEntry, self.xiEntry, self.iterEntry, self.epsilonEntry)
            S.solve()


root = Tk()
gui = GUI(root)
root.mainloop()
