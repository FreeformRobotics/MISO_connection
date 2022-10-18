import numpy as np
from procrustes import permutation_2sided_explicit
import time
import pickle
import sys
sys.path.append('../../IM')
from utils import Test_IF

I, F=Test_IF()

start = time.time()
res = permutation_2sided_explicit(I, F, remove_zero_col=False, remove_zero_row=False)
D_perm2_explicit= np.dot(np.dot(res.t.T, F), res.t)-I
end=time.time()

Time_perm2_explicit=end-start

result=[I, F, res, Time_perm2_explicit]

data_output = open('/data/results/global_procrustes/global_example1.txt', 'wb')
pickle.dump(result, data_output)
data_output.close()



