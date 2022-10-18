# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # import geatpy
import matplotlib.pyplot as plt
from MyProblem import SRP  # Import custom question interface
import progressbar
import pickle


if __name__ == '__main__':
    p = progressbar.ProgressBar()
    N = 1000
    result = []
    for n in p(range(3, N)):
        problem = SRP(n)
        """==================================Population setting=============================="""
        Encoding = 'P'  # Coding method, using permutation coding
        NIND = 50  # Population size
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # Create a region descriptor
        population = ea.Population(Encoding, Field, NIND)  #Instantiate the population object (the population has not been initialized at this time, just complete the instantiation of the population object)
        """================================Algorithm parameter settings============================="""
        myAlgorithm = ea.soea_SEGA_templet(problem, population)
        myAlgorithm.MAXGEN = 200  # Maximum evolutionary generation
        myAlgorithm.mutOper.Pm = 0.5  # Mutation probability
        myAlgorithm.logTras = 1  # Set how many generations to record the log, if set to 0, it means that no log is recorded
        myAlgorithm.verbose = False  # Set whether to print out log information
        myAlgorithm.drawing = 0 # Set the drawing mode (0: no drawing; 1: drawing result diagram; 2: drawing target space process animation; 3: drawing decision space process animation)
        """===========================Population evolution========================"""
        [BestIndi, population] = myAlgorithm.run()
        BestIndi.save()  # Save the information of the best individual to a file
        """==================================Result=============================="""
        print('Module number：%s' % n)
        print('Time has passed %s seconds' % myAlgorithm.passTime)
        if BestIndi.sizes != 0:
            print('The best individual is：%s' % BestIndi.ObjV[0][0])

        result.append([n, BestIndi.ObjV[0][0] ,myAlgorithm.passTime])
        if n%100==0:
            data_output = open('/data/results/Genetic_Algorithm/GA.txt', 'wb')
            pickle.dump(result, data_output)
            data_output.close()
