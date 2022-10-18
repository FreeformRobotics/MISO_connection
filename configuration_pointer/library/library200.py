import time
import pickle
import progressbar
import sys
sys.path.append('../../IM')
from Matrix2tree import Matrix2tree
N = 200
result={}
encode_times=[]

p = progressbar.ProgressBar()
for n in p(range(4, N)):
    data_input = open('/data/Matrix4/'+str(n)+'.txt', 'rb')
    matrices=pickle.load(data_input)
    data_input.close()
    I = matrices[0]
    F = matrices[1]

    data_input = open('/data/results/EXP_Pairing/mat4_'+str(n)+'.txt', 'rb')
    res=pickle.load(data_input)
    data_input.close()
    D= res[0]

    start=time.time()

    A=Matrix2tree(I,'Initial')
    A.matrix2tree(printer=False)
    A.CNL_cal()
    A.tree_render(printer=False, draw=False)
    Asigs=A.Pointer()
    B=Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=False, draw=False)
    Bsigs=B.Pointer()

    instance_pointer=''
    for sig in Asigs:
        instance_pointer = instance_pointer + ''.join((map(str, str(sig))))
    for sig in Bsigs:
        instance_pointer = instance_pointer + ''.join((map(str, str(sig))))
    if instance_pointer=='':
        instance_pointer='0'
    instance_pointer=int(instance_pointer)

    D_p=[]
    D_n=[]
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            if D[i,j]==1:
                D_p.append((i,j))
            if D[i,j]==-1:
                D_n.append((i,j))
    D_compress=[]
    D_compress.append(D_p)
    D_compress.append(D_n)

    result[instance_pointer]=D_compress
    elapsed=time.time()-start
    encode_times.append(elapsed)


data_output = open('/data/results/library200.txt', 'wb')
pickle.dump(result, data_output)
data_output.close()

data_output = open('/data/results/encode_times200.txt', 'wb')
pickle.dump(encode_times, data_output)
data_output.close()
