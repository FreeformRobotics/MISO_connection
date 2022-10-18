import numpy as np
from anytree import AnyNode, RenderTree, PreOrderIter


class CON_Pairing():
    def __init__(self, A, B):
        self.A=A
        self.B=B
        self.n =np.shape(A.matrix)[0]
        #j represents the number of nodes in the common subgraph
        self.j=0
        #i represents the number of virtual grounds
        self.vrm_i=0
        self.virtual_grounds=[]
        #Save all nodes in the common subgraph
        self.csg=[]

    def CNL_match(self, start_csg):
        #Until the end of the leaf node
        if len(self.A.nodes[start_csg.Match[0]].children)==0 or len(self.B.nodes[start_csg.Match[1]].children)==0:
            return

        A_CNL_sorted=[]
        for child in self.A.nodes[start_csg.Match[0]].children:
            A_CNL_sorted.append((child.parent_C, child.ID))
        B_CNL_sorted=[]
        for child in self.B.nodes[start_csg.Match[1]].children:
            B_CNL_sorted.append((child.parent_C, child.ID))

        #For each CN in CNL, sort from largest to smallest
        A_CNL_sorted.sort(key=lambda elem:elem[0], reverse=True)
        B_CNL_sorted.sort(key=lambda elem:elem[0], reverse=True)

        #Match CN in descending order.
        for i in range(min(len(A_CNL_sorted),len(B_CNL_sorted))):
            globals()['con_csg' + str(self.j)] = AnyNode(ID=self.j, name='csg' + str(self.j), parent=start_csg, Match=(A_CNL_sorted[i][1], B_CNL_sorted[i][1]))
            self.j += 1
        #For the already matched CNL, the next level is matched.
        for child in start_csg.children:
            self.CNL_match(child)

    def Virtual_roots(self, printer=True):

        A_index_lef=list(range(self.n))
        B_index_lef=list(range(self.n))

        while len(A_index_lef)!=0:

            globals()['con_A_vrm'+str(self.n+self.vrm_i)]=AnyNode(name='A_vrm'+str(self.n+self.vrm_i), ID=self.n+self.vrm_i, CNL=[], pointer=[], parent_C=None)
            globals()['con_B_vrm'+str(self.n+self.vrm_i)]=AnyNode(name='B_vrm'+str(self.n+self.vrm_i), ID=self.n+self.vrm_i, CNL=[], pointer=[], parent_C=None)
            #For different connected components in the configuration, design a virtual ground for their root modules to suck up.
            for index in A_index_lef:
                if self.A.nodes[index].parent==None or self.A.nodes[index].parent.ID not in A_index_lef:
                    self.A.nodes[index].parent=globals()['con_A_vrm'+str(self.n+self.vrm_i)]
                    globals()['con_A_vrm' + str(self.n+self.vrm_i)].CNL.append(sum(self.A.nodes[index].CNL)+1)
                    self.A.nodes[index].parent_C=len(globals()['con_A_vrm' + str(self.n+self.vrm_i)].CNL)-1

            for index in B_index_lef:
                if self.B.nodes[index].parent==None or self.B.nodes[index].parent.ID not in B_index_lef:
                    self.B.nodes[index].parent=globals()['con_B_vrm'+str(self.n+self.vrm_i)]
                    globals()['con_B_vrm' + str(self.n+self.vrm_i)].CNL.append(sum(self.B.nodes[index].CNL)+1)
                    self.B.nodes[index].parent_C=len(globals()['con_B_vrm' + str(self.n+self.vrm_i)].CNL)-1
            #The nodes of the virtual ground are placed at the end.
            self.A.nodes.append(globals()['con_A_vrm'+str(self.n+self.vrm_i)])
            self.B.nodes.append(globals()['con_B_vrm'+str(self.n+self.vrm_i)])
            #One-to-one pairing of newly added virtual ground
            globals()['con_csg' + str(self.n +self.vrm_i)] = AnyNode(ID=self.n +self.vrm_i, name='csg' + str(self.n +self.vrm_i), Match=(self.n+self.vrm_i, self.n+self.vrm_i))
            self.virtual_grounds.append(self.n+self.vrm_i)
            #The match of the virtual ground is used as the starting node of the next CNL_match.
            self.CNL_match(globals()['con_csg' + str(self.n +self.vrm_i)])
            if printer==True:
                print(RenderTree(globals()['con_csg' + str(self.n +self.vrm_i)]))
            self.vrm_i += 1

            A_index_del = [node.Match[0] for node in PreOrderIter(globals()['con_csg' + str(self.virtual_grounds[-1])])]
            B_index_del = [node.Match[1] for node in PreOrderIter(globals()['con_csg' + str(self.virtual_grounds[-1])])]
            A_index_lef = (set(A_index_lef).difference(set(A_index_del)))
            B_index_lef = (set(B_index_lef).difference(set(B_index_del)))
        #Save all matches except virtual grounds.
        for i in range(self.n):
            self.csg.append(globals()['con_csg' + str(i)])

    def Difference(self, printer=True):
        #Sort the ID numbers in the final configuration according to the new match.
        seqbak=[]
        for c in range(len(self.csg)):
            seqbak.append(self.csg[c].Match)

        def takeFirst(elem):
            return elem[0]

        seqbak.sort(key=takeFirst)

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
        #The disconnected connection in the initial configuration is disconnected,
        #The disconnected connection in the final configuration is reconnected.
        for tu in self.A.disconnect:
            if self.D[tu[0]][tu[1]] != -1:
                self.D[tu[0]][tu[1]] -= 1
        for tu in self.B.disconnect:
            if self.D[sequence.index(tu[0])][sequence.index(tu[1])] != 1:
                self.D[sequence.index(tu[0])][sequence.index(tu[1])] += 1
        #print(self.D)
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





