import sys
sys.path.append('../IM')
from utils import Matrix_gen_B_explicit
import pickle
import progressbar
import random

n=31
b_max = 13
p = progressbar.ProgressBar()
for diff in p(range(3, b_max-4)):
    b1=random.randint(3, b_max-diff)
    b2=b1+diff
    I = Matrix_gen_B_explicit(n, b1)
    F = Matrix_gen_B_explicit(n, b2)

    result=[I, F]

    data_output = open('../../data/Matrix24/'+str(diff)+'.txt', 'wb')
    pickle.dump(result, data_output)
    data_output.close()
