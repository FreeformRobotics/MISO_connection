import time
import pickle
import progressbar
import Matrix2tree
import Greedy_CM
from utils import Test_IF

N = 1000
p = progressbar.ProgressBar()
for n in p(range(3, N)):
    data_input = open('../../data/Matrix1/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]
# I, F=Test_IF()
# n=12
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


    test_cm=Greedy_CM.CM(A, B)

    test_cm.UV(printer=False)
    D, error_cm=test_cm.Difference(printer=False)

    time_cm = time.time() - start

    result=[error_cm, time_cm]

    data_output = open('../../data/results/Greedy_CM/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
