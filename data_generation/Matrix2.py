import sys
sys.path.append('../IM')
from utils import Matrix_gen_B
import pickle
import progressbar

n = 1000
p = progressbar.ProgressBar()
for b in p(range(3, 1000)):
    I = Matrix_gen_B(n, b)
    F = Matrix_gen_B(n, b)

    result=[I, F]

    data_output = open('../../data/Matrix2/'+str(b)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
