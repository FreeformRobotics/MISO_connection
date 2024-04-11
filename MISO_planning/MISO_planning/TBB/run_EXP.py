from MISO_planning.IM import Matrix2tree
from MISO_planning.IM.utils import Matrix_gen
from MISO_planning.TBB.EXP_Pairing import EXP_Pairing

def TBB(I,F):
    A=Matrix2tree.Matrix2tree(I,'Initial')
    A.matrix2tree(printer=False)
    A.CNL_cal()
    A.tree_render(printer=False, draw=False)

    B=Matrix2tree.Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=False, draw=False)
    #if the IM algorithm is run, its final error could be served as the IM_bound below.
    test_exp= EXP_Pairing(A, B, IM_bound=I.shape[0])
    test_exp.EXP_pairing(printer=False)

    #if the initial configuration or final configuration has circuits, error_D is not equal to error_exp.
    D, error_D = test_exp.Difference(printer=False)
    error_exp=test_exp.UPPER
    return D, error_exp

if __name__ == '__main__':
    n = 10
    I = Matrix_gen(n)
    F = Matrix_gen(n)
    D, error = TBB(I, F)



