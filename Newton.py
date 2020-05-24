import  numpy as np
import matplotlib.pyplot as plt

class Newton :
    DivDeff = None
    X = None
    Y = None
    n = None
    def __init__(self,X,Y,n):
        self.X = X;self.Y = Y;self.n = n
        self.DivDeff = np.zeros((n,n))
        self.newtonInterpolation()
        self.createDividedDiffTable()
        print("Div Deff Table Is : ")
        self.printDivDeff()
        # print(self.createFormula())

    def newtonInterpolation(self):
        for i in range (0,self.n):
            self.DivDeff[i][0] = self.Y[i]
            # print(self.DivDeff[i][0])

    def createDividedDiffTable(self):
        # self.DivDeff[0][1] = self.DivDeff[0][1]
        for j in range (1,self.n):  #LL columns 3alashan l column 0 ll inputs
            for i in range (j,self.n): #ll rows
                self.DivDeff[i][j] = (self.DivDeff[i][j-1]-self.DivDeff[i-1][j-1])/(self.X[i]-self.X[i-j])

    def createFormula(self):
        funString = ""
        for i in range (0,self.n):
            if (self.DivDeff[i][i] == 0):
                continue
            funString += str(self.DivDeff[i][i])
            for j in range (0,i):
                funString += "(x - "+str(self.X[j])+")"
            funString += "+"
        funString = funString[:-1]
        return funString

    def printDivDeff(self):
        for i in range(self.n):
            for j in range(0,self.n):
                print(round(self.DivDeff[i][j], 4), "\t",end=" ")
            print("")

    def solve(self,x):
        # print("X is "+str(x))
        output = 0.0
        for i in range (0,self.n):
            term = self.DivDeff[i][i]
            for j in range (0,i):
                term *= (x - self.X[j])
            # print("term is "+str(term))
            output += term
        return output

    def plot(self):
        step = (self.X[0] - self.X[len(self.X) - 1]) / 10000
        values_x = []
        values_y = []
        for i in range(10000 + 3):
            values_y.append(self.solve(self.X[0] + step * i))
            values_x.append(self.X[0] + step * i)
        plt.plot(values_x, values_y)
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("graph!")
        plt.show()

n =6;
Y = [ 7.2,7.1,6.0,5.0,3.5,5.0 ]
X = [ 2.0,4.25,5.25,7.81,9.2,10.6  ];
# Newton(X,Y,n)
# Newton.printDivDeff()
