import time
import pickle
import sys
sys.path.append('../IM')
from Matrix2tree import Matrix2tree
from CON_Pairing import CON_Pairing
from CNL_Pairing import CNL_Pairing
from utils import human_I_568, human_F_568

# F = Matrix_gen(500)
# data_output = open('final_matrix.txt', 'wb')
# pickle.dump(F, data_output)
# data_output.close()
# data_input = open('final_matrix.txt', 'rb')
# F = pickle.load(data_input)
# data_input.close()
F=human_F_568()
I = human_I_568()

start = time.time()

A=Matrix2tree(I,'Initial')
A.matrix2tree(printer=False)
A.CNL_cal()
A.tree_render(printer=False, draw=False)

B=Matrix2tree(F, 'Final')
B.matrix2tree(printer=False)
B.CNL_cal()
B.tree_render(printer=False, draw=False)

test_con=CON_Pairing(A, B)
test_con.Virtual_roots(printer=True)
D_con, error_con=test_con.Difference(printer=False)

time_con = time.time() - start

result=[D_con, error_con]
data_output = open('/data/results/human_con.txt', 'wb')
pickle.dump(result, data_output)
data_output.close()

# test_cnl=CNL_Pairing(A, B)
# test_cnl.Virtual_roots(printer=True)
# D_cnl, error_cnl=test_cnl.Difference(printer=False)
#
# time_cnl = time.time() - start
#
# result=[D_cnl, error_cnl]
# data_output = open('/data/results/human_cnl.txt', 'wb')
# pickle.dump(result, data_output)
# data_output.close()
