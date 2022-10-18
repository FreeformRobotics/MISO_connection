from procrustes import permutation_2sided_explicit
import time
import pickle
import sys
sys.path.append('../../IM')
from utils import Matrix_gen

N=100
for n in range(3, N):
    I=Matrix_gen(n)
    F=Matrix_gen(n)

    start = time.time()
    res = permutation_2sided_explicit(I, F, remove_zero_col=False, remove_zero_row=False)
    # D_perm2_explicit= np.dot(np.dot(res.t.T, F), res.t)-I
    end=time.time()

    Time_perm2_explicit=end-start

    result=[I, F, res.t, Time_perm2_explicit]
    print('n:{}'.format(n))
    data_output = open('/data/results/global_procrustes/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()



