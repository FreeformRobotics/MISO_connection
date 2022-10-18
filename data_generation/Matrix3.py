import sys
sys.path.append('../IM')
from utils import Matrix_gen_B_explicit

import pickle
import progressbar

n = 1000
p = progressbar.ProgressBar()
for b in p(range(3, 489)):
    I = Matrix_gen_B_explicit(n, b)
    F = Matrix_gen_B_explicit(n, b)

    result=[I, F]

    data_output = open('../../data/Matrix3/'+str(b)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
