import numpy as np
from scipy.optimize import quadratic_assignment
from con_planning.utils import Test_IF

A, B=Test_IF()
res = quadratic_assignment(A, B)
print(res)
perm = res['col_ind']
P = np.eye(len(A), dtype=int)[perm]
guess = np.array([np.arange(len(A)), res.col_ind]).T
res = quadratic_assignment(A, B, method="2opt", options = {'partial_guess': guess})
