from tkinter import *
from tkinter import ttk, filedialog
import numpy as np
import tabulate
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Open_methods import FixedPoint, NewtonRaphson, Secant
import Lagrange
import Newton
import random


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
        i = 1
        self.v.set(4)
        # ct = [100,50,70]
        # #brightness = int(round(0.299 * ct[0] + 0.587 * ct[1] + 0.114 * ct[2]))
        # ct_hex = "%02x%02x%02x" % tuple(ct)
        # bg_colour = '#' + "".join(ct_hex)
        for text, mode in MODES:
            i += 1
            Radiobutton(self.part1, text=text,
                        variable=self.v, value=mode,
                        command=lambda: GUI.clicked(self, self.v.get()),
                        fg="black", bg="cadet blue", font="Times 14", indicatoron=False).place(x=20,
                                                                                               y=50 * i)


    def clicked(self, value):
        fxlabel = Label(self.part1, text="F(x)", font="Times 11")
        gxlabel = Label(self.part1, text="g(x)", font="Times 11")
        xilabel = Label(self.part1, text="Initial Approximation", font="Times 11").place(x=175, y=150)
        xprevlabel = Label(self.part1, text="Previous Approximation", font="Times 11").place(x=175, y=200)
        iterlabel = Label(self.part1, text="max iterations", font="Times 11").place(x=175, y=250)
        epsilonlabel = Label(self.part1, text="epsilon", font="Times 11").place(x=175, y=300)

        self.func = StringVar()
        self.xi = DoubleVar()
        self.xprev = DoubleVar()
        self.maxiter = IntVar()
        self.maxiter.set(0)
        self.epsilon = DoubleVar()
        self.epsilon.set(0)
        Entry1 = Entry(self.part1, width=30, textvariable=self.func).place(x=320, y=100)
        xiEntry = Entry(self.part1, width=30, textvariable=self.xi).place(x=320, y=150)
        xprevEntry = Entry(self.part1, width=30, textvariable=self.xprev)
        xprevEntry.place(x=320, y=200)
        iterEntry = Entry(self.part1, width=30, textvariable=self.maxiter).place(x=320, y=250)
        epsilonEntry = Entry(self.part1, width=30, textvariable=self.epsilon).place(x=320, y=300)

        button = Button(self.part1, width=10, height=1, text="Solve", command=self.solveP2, bg="cadet blue", font="Times 13").place(x=450, y=350)

        if self.v.get() == 1:
            print(1)
        elif self.v.get() == 2:
            print(2)
        elif self.v.get() == 3:
            fxlabel.config(DISABLED)
            xprevEntry.config(state='disabled')
            gxlabel.place(x=175, y=100)
        elif self.v.get() == 4:
            gxlabel.config(DISABLED)
            xprevEntry.config(state='disabled')
            fxlabel.place(x=175, y=100)
        elif self.v.get() == 5:
            gxlabel.config(DISABLED)
            xprevEntry.config(state='normal')
            fxlabel.place(x=175, y=100)

    def readInput(self, entry):
        self.polynomiaOrder = int(entry.widget.get())
        columnLabel = 0
        columnX = 1
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

        x = float((self.solve_for_x_entry).get())
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
        self.windowp2 = Toplevel(root)
        self.windowp2.title("Root Finder")
        self.windowp2.geometry('1200x600')

        if self.v.get() == 3:
            F = FixedPoint.FP(self.func.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            self.max = 3
            self.Result = F.solve()
        elif self.v.get() == 4:
            N = NewtonRaphson.NR(self.func.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            self.max = 3
            self.Result = N.solve()
        elif self.v.get() == 5:
            S = Secant.SC(self.func.get(), self.xprev.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            self.max = 4
            self.Result = S.solve()
        GUI.tableP2(self)

    def tableP2(self):
        number_of_iterations = self.Result[0]
        execution_time = self.Result[1]
        iterations = self.Result[2]
        xr = self.Result[3]
        ea = self.Result[4]

        button = Button(self.windowp2, width=10, height=1, text="Plot", command=lambda:GUI.plotP2(self), bg="cadet blue", font="Times 13").place(x=950, y=350)

        label = Label(self.windowp2, text="Xr = " + str(xr), bg="cadet blue", fg="black", width=30).place(x=950,y=100)
        label = Label(self.windowp2, text="Number of iterations = " + str(number_of_iterations), bg="cadet blue", fg="black", width=30).place(x=950,y=150)
        label = Label(self.windowp2, text="Execution Time = " + str(execution_time), bg="cadet blue", fg="black", width=30).place(x=950,y=200)
        label = Label(self.windowp2, text="ea = " + str(ea), bg="cadet blue", fg="black", width=30).place(x=950,y=250)

        if self.max == 3:
            label = Label(self.windowp2, text="i", bg="black", fg="white", width=10)
            label.grid(row=0, column=0)
            label = Label(self.windowp2, text="Current Approximation", bg="black", fg="white", width=30)
            label.grid(row=0, column=1)
            label = Label(self.windowp2, text="Approximate Root", bg="black", fg="white", width=30)
            label.grid(row=0, column=2)
            label = Label(self.windowp2, text="Error", bg="grey", fg="white", width=30)
            label.grid(row=0, column=3)
        if self.max == 4:
            label = Label(self.windowp2, text="i", bg="grey", fg="white", width=10)
            label.grid(row=0, column=0)
            label = Label(self.windowp2, text="Previous Approximation", bg="black", fg="white", width=30)
            label.grid(row=0, column=1)
            label = Label(self.windowp2, text="Current Approximation", bg="black", fg="white", width=30)
            label.grid(row=0, column=2)
            label = Label(self.windowp2, text="Approximate Root", bg="black", fg="white", width=30)
            label.grid(row=0, column=3)
            label = Label(self.windowp2, text="Error", bg="grey", fg="white", width=30)
            label.grid(row=0, column=4)

        column = 0
        for row in range(len(iterations)):
            iteration = iterations[row]
            if self.max == 3:
                label = Label(self.windowp2, text=row, bg="black", fg="white", width=10)
                label.grid(row=row+1, column=column)
                label = Label(self.windowp2, text=iteration['current_approximate'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column+1)
                label = Label(self.windowp2, text=iteration['approximate_root'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column + 2)
                label = Label(self.windowp2, text=iteration['error'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column + 3)
            if self.max == 4:
                label = Label(self.windowp2, text=row, bg="black", fg="white", width=10)
                label.grid(row=row + 1, column=column)
                label = Label(self.windowp2, text=iteration['previous_approximate'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column+1)
                label = Label(self.windowp2, text=iteration['current_approximate'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column + 2)
                label = Label(self.windowp2, text=iteration['approximate_root'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column + 3)
                label = Label(self.windowp2, text=iteration['error'], bg="white", fg="black", width=30)
                label.grid(row=row+1, column=column + 4)

    def plotP2(self):
        if self.v.get() == 1:
             print(1)
        elif self.v.get() == 2:
            print(2)
        elif self.v.get() == 3:
            F = FixedPoint.FP(self.func.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            F.draw_plot(self.Result[2], self.Result[5])
        elif self.v.get() == 4:
            N = NewtonRaphson.NR(self.func.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            N.draw_plot(self.Result[2], self.Result[5])
        elif self.v.get() == 5:
            S = Secant.SC(self.func.get(), self.xprev.get(), self.xi.get(), self.maxiter.get(), self.epsilon.get())
            S.draw_plot(self.Result[2], self.Result[5])





root = Tk()
gui = GUI(root)
root.mainloop()
