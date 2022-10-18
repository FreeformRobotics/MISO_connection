import math
import time
import pickle
import progressbar
import sys
sys.path.append('../IM')
import Matrix2tree
import EXP_Pairing
import datetime
import multiprocessing as mp


def train_on_parameter(n):
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

    test_exp=EXP_Pairing.EXP_Pairing(A, B)

    test_exp.EXP_pairing(printer=False)
    error_exp=test_exp.UPPER
    time_exp = time.time() - start

    result=[error_exp, time_exp]


    data_output = open('../../data/results/EXP_Pairing/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
    return time_exp

if __name__ == '__main__':

    num_cores = int(mp.cpu_count())-6
    pool = mp.Pool(num_cores)

    results=[pool.apply_async(train_on_parameter, args=(n, )) for n in range(34, 36)]
    print([res.get() for res in results])
