from MISO_planning.IM import Matrix2tree
from MISO_planning.IM import CNL_Pairing
from MISO_planning.IM.utils import Matrix_gen

def IM(I, F):
    A = Matrix2tree.Matrix2tree(I, 'Initial')
    A.matrix2tree(printer=False)
    A.CNL_cal()
    A.tree_render(printer=False, draw=False)
    A.Pointer()
    A.Pointer_int(printer=False)

    B = Matrix2tree.Matrix2tree(F, 'Final')
    B.matrix2tree(printer=False)
    B.CNL_cal()
    B.tree_render(printer=False, draw=False)
    B.Pointer()
    B.Pointer_int(printer=False)

    test_cnl = CNL_Pairing.CNL_Pairing(A, B)

    test_cnl.Virtual_roots(printer=False)
    D, error_cnl = test_cnl.Difference(printer=False)
    return D, error_cnl

if __name__ == '__main__':
    n=12
    I = Matrix_gen(n)
    F = Matrix_gen(n)
    D, error_cnl=IM(I, F)
    print("error_cnl:{}".format(error_cnl))


