from  tkinter import *
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
import Lagrange
import Newton
class GUI :
    master = None
    part1 = None
    part2 = None

    polynomiaOrder = None
    def __init__ (self,master):
        self.master = master
        master.title("Numerical Project")
        master.geometry('500x500')
        self.createTabs()
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
        self.polyOrderEntry = Entry(self.part2,width = 10)
        self.polyOrderEntry.grid(column=1, row=0,padx=10, pady=10)
        self.polyOrderEntry.bind("<Return>", self.readInput)
        orLabel = Label(self.part2, text="Or").grid(column=3, row=0, padx=10, pady=10)
        read_button = Button(self.part2, width=20, height=1, text="Read data from file", command=self.readFromFile).grid(row=0, column=4)

    def readInput(self,entry):
        self.polynomiaOrder = int(entry.widget.get())
        columnLabel = 0;columnX = 1;columnY =2
        row = 1
        self.entryX = [None] * (self.polynomiaOrder)
        self.entryY = [None] * (self.polynomiaOrder)
        for i in range (1,self.polynomiaOrder+1) :
            label = Label(self.part2, text=("Point number "+str(i))).grid(column=columnLabel, row=(row+i), padx=10, pady=10)
            self.entryX[i-1] = Entry(self.part2,width = 10)
            self.entryX[i-1].grid(column=columnX, row=(row+i), padx=5, pady=5)

            self.entryY[i-1] = Entry(self.part2,width = 10)
            self.entryY[i-1].grid(column=columnY, row=(row + i), padx=5, pady=5)

            if ((i!=0)and(i%15==0)):
                columnLabel+=3;columnX+=3;columnY+=3
                row = 1-i

        self.completePart2(columnY,row+self.polynomiaOrder+1)

    def completePart2(self,column,row):
        solve_for_x = Label(self.part2, text="Find value for    ").grid(row=row,column = column-2)
        self.solve_for_x_entry = Entry(self.part2,width = 25)
        self.solve_for_x_entry.grid(column=column-1, row=row, padx=5, pady=5,columnspan = 2)

        self.var = IntVar()
        R1 = Radiobutton(self.part2, text="newton", variable=self.var, value=1).grid(row=row+1, column=column-1)
        R2 = Radiobutton(self.part2, text="lagrange", variable=self.var, value=2).grid(row=row+2, column=column-1)

        solve_button = Button(self.part2, width=10, height=1, text="solve", command=self.solve).grid(column=column, row=row+2, padx=10, pady=10)

    def readFromFile():
        X = []
        Y = []
        t = 0
        file_path = filedialog.askopenfilename()
        # read_from_file(file_path)

        f = open(file_path, "r")
        i = 0
        for x in f:
            if i == 0:
                T = float(x)
                i += 1
            else:
                a = x.split(" ")
                X.append(float(a[0]))
                Y.append(float(a[1]))
        l = Lagrange(X, Y, T)
        l.lagrange()
        value = Label(root, text=l.calc_value(T))
        value.grid(row=5)
        poly = Label(root, text=l.poly())
        poly.grid(row=6)
        l.plot()

    def solve(self):
        X = [None] * (self.polynomiaOrder)
        Y = [None] * (self.polynomiaOrder)
        for i in range(1,self.polynomiaOrder+1):
            X[i-1] = float((self.entryX[i-1]).get())
            Y[i-1] = float((self.entryY[i-1]).get())
            # print(X[i-1]+" "+Y[i-1])

        x = float((self.solve_for_x_entry).get())
        window = Toplevel(root)
        window.title("Newton")
        window.geometry('500x500')
        functionLabel = Label(window, text="Output function ").grid(row=0, column=1)
        solveLabel = Label(window, text=("Output at X = " + str(x))).grid(row=1, column=1)

        if self.var.get() == 2:
            l = Lagrange.Lagrange(X,Y,x)
            l.lagrange()
            outputLabel = Label(window, text=str(l.poly())).grid(row=0, column=3)
            solveOutput = Label(window, text=(str(l.calc_value(x)))).grid(row=1, column=3)
            l.plot()
        if self.var.get() == 1 :
            n = Newton.Newton(X,Y,self.polynomiaOrder)
            outputLabel = Label(window, text=str(n.createFormula())).grid(row=0,column = 3)
            solveOutput = Label(window, text=(str(n.solve(x)))).grid(row=1, column=3)

root = Tk()
gui = GUI(root)
root.mainloop()
