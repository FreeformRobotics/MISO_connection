import sys

sys.path.append('../../IM')
from utils import Test_IF

def diff_vars(a, b):
    _, F =Test_IF()
    if F[a, b]==1:# the same adjacent connection
        cost=0
    else:
        cost=1
    return cost
