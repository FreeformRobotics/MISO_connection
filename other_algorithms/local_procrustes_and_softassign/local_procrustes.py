from procrustes import permutation_2sided
import time
import pickle
import progressbar

N = 1000
p = progressbar.ProgressBar()
for n in p(range(4, N)):
    data_input = open('/data/Matrix1/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()

    I = matrices[0]
    F = matrices[1]

    start = time.time()

    res_perm2 = permutation_2sided(I, F, remove_zero_col=False, remove_zero_row=False, mode='normal1')
    error_perm = res_perm2.error
    time_perm = time.time()-start

    result=[error_perm, time_perm]

    data_output = open('/data/results/local_procrustes/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
