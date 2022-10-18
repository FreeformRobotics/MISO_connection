import time
import pickle
import progressbar
import sys
sys.path.append('../IM')
from Matrix2tree import Matrix2tree

N = 200
read_times=[]


p = progressbar.ProgressBar()
for n in p(range(4, N)):
    data_input = open('/data/Matrix4/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]

    data_input = open('/data/results/library200.txt', 'rb')
    library=pickle.load(data_input)
    data_input.close()

    start=time.time()

    A=Matrix2tree(I,'Initial')
    A.matrix2tree(printer=False)
    A.CNL_cal()
    A.tree_render(printer=True, draw=False)
    Asigs=A.Pointer()
    B=Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=True, draw=False)
    Bsigs=B.Pointer()

    instance_pointer=''
    for sig in Asigs:
        instance_pointer = instance_pointer + ''.join((map(str, str(sig))))
    for sig in Bsigs:
        instance_pointer = instance_pointer + ''.join((map(str, str(sig))))
    if instance_pointer=='':
        instance_pointer='0'
    instance_pointer=int(instance_pointer)


    D_c=library[instance_pointer]
    elapsed=time.time()-start
    read_times.append(elapsed)

data_output = open('/data/results/read_times200.txt', 'wb')
pickle.dump(read_times, data_output)
data_output.close()

