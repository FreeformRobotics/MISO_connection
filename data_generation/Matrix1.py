import sys
sys.path.append('../IM')
from utils import Matrix_gen

import pickle
import progressbar

N = 1000
p = progressbar.ProgressBar()
for n in p(range(3, N)):
    I = Matrix_gen(n)
    F = Matrix_gen(n)

    result=[I, F]

    data_output = open('../../data/Matrix1/'+str(n)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
