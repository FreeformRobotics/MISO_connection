import time
import pickle
import progressbar
import Matrix2tree
import CON_Pairing

N = 31
p = progressbar.ProgressBar()
for n in p(range(3, N)):
    data_input = open('../../data/Matrix22/'+str(n)+'.txt', 'rb')
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

    test_con=CON_Pairing.CON_Pairing(A, B)

    test_con.Virtual_roots(printer=False)
    _, error_con=test_con.Difference(printer=False)

    time_con = time.time() - start

    result=[error_con, time_con]

    data_output = open('../../data/results/CON_Pairing/Matrix22_'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
