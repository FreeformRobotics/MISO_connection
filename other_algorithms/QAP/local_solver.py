########## qap.py ##########

import localsolver
import pickle
import progressbar

N = 1000
p = progressbar.ProgressBar()


for n in p(range(10, N)):
    data_input = open('../../../data/Matrix6/' + str(n) + '.txt', 'rb')
    matrices = pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]

    with localsolver.LocalSolver() as ls:

        # Distance between locations
        A = [[I[i][j] for j in range(n)] for i in range(n)]
        # Flow between factories
        B = [[F[i][j] for j in range(n)] for i in range(n)]

        # Declares the optimization model
        model = ls.model

        # Permutation such that p[i] is the facility on the location i
        p = model.list(n)

        # The list must be complete
        model.constraint(model.eq(model.count(p), n))

        # Create B as an array to be accessed by an at operator
        array_B = model.array(model.array(B[i]) for i in range(n))

        # Minimize the sum of product distance*flow
        obj = model.sum(-A[i][j]*model.at(array_B, p[i], p[j]) for j in range(n) for i in range(n))
        model.minimize(obj)

        model.close()

        ls.param.time_limit = n*5
        ls.solve()

        #
        # Writes the solution in a file with the following format:
        #  - n objValue
        #  - permutation p
        #
        with open('../../../data/results/QAP/'+str(n)+'.txt', 'w') as outfile:
            outfile.write("%d %d\n" % (n, obj.value))
            for i in range(n):
                outfile.write("%d " % p.value[i])
            outfile.write("\n")