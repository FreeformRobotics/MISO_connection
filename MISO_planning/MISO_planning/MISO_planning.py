from MISO_planning.IM.utils import Matrix_gen
from MISO_planning.IM.run_IM import IM
from MISO_planning.TBB.run_EXP import TBB

def MISO_planning(I, F, run_TBB=False):
    #For the TBB algorithm, the number of modules should be less than 35, recommended limitation is 25.
    if run_TBB==True and I.shape[0]<=25:
        D, error= TBB(I, F)
    #For the IM algorithm, the number of modules is not limited, could be larger than 1000 or more.
    else:
        D, error = IM(I, F)
    return D, error

if __name__ == '__main__':
    n = 20
    I = Matrix_gen(n)
    F = Matrix_gen(n)
    D, error = MISO_planning(I, F, run_TBB=False)
    print("error:{}".format(error))



