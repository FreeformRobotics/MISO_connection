import time
import pickle
import progressbar
from procrustes import softassign

N = 141
p = progressbar.ProgressBar()
for n in p(range(4, N)):
    data_input = open('/data/Matrix1/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]
    start = time.time()
    res_soft = softassign(I, F, remove_zero_col=False, remove_zero_row=False)
    error_soft=res_soft.error
    time_soft=time.time()-start

    result=[error_soft, time_soft ]

    data_output = open('/data/results/softassign/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
