import pickle
import progressbar
from numpy import linalg as LA

N = 489
p = progressbar.ProgressBar()
for n in p(range(4, N)):
    data_input = open('/data/Matrix1/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]

    w1, v1 =LA.eig(I)
    w2, v2 =LA.eig(F)

    print(w1, w2)


