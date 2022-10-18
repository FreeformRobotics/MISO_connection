import time
import pickle
import progressbar
import Matrix2tree
import POINTER_Pairing

N = 1000
p = progressbar.ProgressBar()
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
    A.Pointer()
    Asigs=A.Pointer_int(printer=False)

    B=Matrix2tree.Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=False, draw=False)
    B.Pointer()
    Bsigs=B.Pointer_int(printer=False)


    test_cnl=POINTER_Pairing.POINTER_Pairing(A, B)

    test_cnl.Virtual_roots(printer=False)
    D, error_cnl=test_cnl.Difference(printer=False)

    time_cnl = time.time() - start

    result=[error_cnl, time_cnl]

    data_output = open('../../data/results/POINTER_Pairing/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
