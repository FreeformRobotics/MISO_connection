# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
import sys
sys.path.append('../../IM')
from utils import Test_IF, Test_IF_500, Matrix_gen

class SRP(ea.Problem):  # Inherit the Problem parent class
    def __init__(self, N):
        name = 'SRP'
        self.N=N
        M = 1  # Target dimension
        maxormins = [1]  # 1: minimize the target; -1: maximize the target
        Dim = N  # dimension of decision variable
        varTypes = [1] * Dim  #The type of decision variable, the element is 0 means that the corresponding variable is continuous; 1 means that it is discrete
        lb = [0] * Dim  # Lower bound of decision variables
        ub = [N] * Dim  # Upper bound of decision variable
        lbin = [1] * Dim  # 0 means not including the lower boundary of the variable, 1 means including
        ubin = [0] * Dim  # 0 means not including the upper boundary of the variable, 1 means including
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # target function
        x = pop.Phen  # Get the decision variable matrix
        ObjV = []
        I= Matrix_gen(self.N)
        F= Matrix_gen(self.N)
        for s in range(x.shape[0]):
            F_new = np.zeros((F.shape[0], F.shape[0]))
            for i in range(F.shape[0]):
                #Adjust the adjacency matrix of the final configuration according to the new ID sequence
                if F[i, :].any() != 0:
                    j = list(F[i, :]).index(1)  # be attached, (i,j)
                    F_new[list(x[s,:]).index(i), list(x[s,:]).index(j)] = 1
            D=F_new - I
            error= int(np.linalg.norm(D, ord='fro') ** 2)
            ObjV.append(error)

        pop.ObjV = np.array([ObjV]).T  # Assign the obtained objective function value to ObjV of population pop
