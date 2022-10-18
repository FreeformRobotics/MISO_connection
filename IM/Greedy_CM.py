import numpy as np
from anytree import AnyNode, RenderTree, PreOrderIter

class CM():
    def __init__(self, A, B):
        self.A=A
        self.B=B
        self.n =np.shape(A.matrix)[0]
        #j represents the number of nodes in the common subgraph
        self.j=0
        self.uv_j=0
        self.matching_set=[[],[]]
        #Save all nodes in the common subgraph
        self.csg=[]



    def MCESC_UV(self, start_csg):
        #Until the end of the leaf node
        if len(self.A.nodes[start_csg.Match[0]].children)==0 or len(self.B.nodes[start_csg.Match[1]].children)==0:
            return

        for child_a in self.A.nodes[start_csg.Match[0]].children:
            for child_b in self.B.nodes[start_csg.Match[1]].children:
                if child_a.parent_C==child_b.parent_C and child_a.ID not in self.matching_set[0] and child_b.ID not in self.matching_set[1]:
                    self.j += 1
                    globals()['csg' + str(self.j)] = AnyNode(ID=self.j, name='csg' + str(self.j), parent=start_csg, Match=(child_a.ID, child_b.ID))
                    self.matching_set[0].append(child_a.ID)
                    self.matching_set[1].append(child_b.ID)

        if self.A.nodes[start_csg.Match[0]].parent != None and self.B.nodes[start_csg.Match[1]].parent!=None:
            active_a_ID=self.A.nodes[start_csg.Match[0]].parent.ID
            active_b_ID=self.B.nodes[start_csg.Match[1]].parent.ID
            if  active_a_ID not in self.matching_set[0] and active_b_ID not in self.matching_set[1]:
                self.j += 1
                globals()['csg' + str(self.j)] = AnyNode(ID=self.j, name='csg' + str(self.j), parent=start_csg, Match=(active_a_ID, active_b_ID))
                self.matching_set[0].append(active_a_ID)
                self.matching_set[1].append(active_b_ID)
        #For the already matched CNL, the next level is matched.
        for child in start_csg.children:
            self.MCESC_UV(child)

    def UV(self, printer=True):
        A_index_lef=list(range(self.n))
        B_index_lef=list(range(self.n))
        A_index_del=[]
        B_index_del=[]

        while len(A_index_lef)!=0:
            #One-to-one pairing
            root_modules=[]
            for mod in A_index_lef:
                if self.A.nodes[mod].parent==None or self.A.nodes[mod].parent.ID in A_index_del:
                    root_modules.append(mod)
            len_root=[]
            for root in root_modules:
                len_vac=[]
                for vac in B_index_lef:
                    self.j += 1
                    globals()['csg' + str(self.j)] = AnyNode(ID=self.j, name='csg' + str(self.j), Match=(mod, vac))
                    #The match is used as the starting node of the next CNL_match.
                    self.matching_set=[A_index_del+[root], B_index_del+[vac]]
                    self.MCESC_UV(globals()['csg' + str(self.j)])
                    len_vac.append((len(self.matching_set[0]), self.matching_set))
                len_vac.sort(key=lambda elem:elem[0])
                len_root.append(len_vac[-1])
            len_root.sort(key=lambda elem:elem[0])
            MCESC=len_root[-1][1]

            if printer==True:
                print(RenderTree(globals()['csg' + str(self.j)]))

            A_index_del = MCESC[0]
            B_index_del = MCESC[1]
            A_index_lef = (set(A_index_lef).difference(set(A_index_del)))
            B_index_lef = (set(B_index_lef).difference(set(B_index_del)))

        self.results=MCESC

    def Difference(self, printer=True):
        #Sort the ID numbers in the final configuration according to the new match.
        seqbak=[]
        for c in range(self.n):
            seqbak.append((self.results[0][c], self.results[1][c]))


        seqbak.sort(key=lambda elem:elem[0])

        sequence=[]
        for s in seqbak:
            sequence.append(s[1])

        X2_new = np.zeros((self.n, self.n))
        for i in range(self.n):
            #Adjust the adjacency matrix of the final configuration according to the new ID sequence
            if self.B.matrix[i, :].any() != 0:
                j = list(self.B.matrix[i, :]).index(1)  # be attached, (i,j)
                X2_new[sequence.index(i), sequence.index(j)] = 1
        self.D=X2_new - self.A.matrix

        error= int(np.linalg.norm(self.D, ord='fro') ** 2)
        if printer==True:
            print('error:{}'.format(error))
        return self.D, error

    def lower_bound(self, printer=True):
        A_C=[0]*7
        for j in range(self.n):
            A_C[int(np.sum(self.A.matrix[:,j]))] += 1
        B_C=[0]*7
        for j in range(self.n):
            B_C[int(np.sum(self.B.matrix[:,j]))] += 1

        for i in range(1, 7):
            A_C[i] += sum(A_C[i+1:])
            B_C[i] += sum(B_C[i+1:])
        lower_b=np.sum(abs(np.array(A_C)-np.array(B_C)))
        if printer==True:
            print('lower bound: {}'.format(lower_b))
        return lower_b






