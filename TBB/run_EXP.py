import sys
sys.path.append('../IM')
import Matrix2tree
import time
import pickle
import progressbar
import EXP_Pairing
p = progressbar.ProgressBar()

N=33
for n in p(range(3, N)):
    data_input = open('../../data/Matrix1/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]

    start = time.time()

    A=Matrix2tree.Matrix2tree(I,'Initial')
    A.matrix2tree(printer=False)
    A.CNL_cal()
    A.tree_render(printer=False, draw=False)

    B=Matrix2tree.Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=False, draw=False)

    test_exp=EXP_Pairing.EXP_Pairing(A, B, matrix_type='Matrix22_')

    test_exp.EXP_pairing(printer=False)
    error_exp=test_exp.UPPER
    time_exp = time.time() - start

    result=[error_exp, time_exp]


    data_output = open('../../data/results/EXP_Pairing/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()



