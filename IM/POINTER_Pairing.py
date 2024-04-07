import numpy as np
from anytree import AnyNode, RenderTree, PreOrderIter
import networkx as nx



class POINTER_Pairing():
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

    def POINTER_pair(self, start_csg):
        #Until the end of the leaf node
        if len(self.A.nodes[start_csg.Match[0]].children)==0 or len(self.B.nodes[start_csg.Match[1]].children)==0:
            return

        A_CNL=[]
        for child in self.A.nodes[start_csg.Match[0]].children:
            A_CNL.append(child)

        B_CNL=[]
        for child in self.B.nodes[start_csg.Match[1]].children:
            B_CNL.append(child)

        Bipartite_Graph = nx.Graph()

        Bipartite_Graph.add_nodes_from(A_CNL, bipartite=0)
        Bipartite_Graph.add_nodes_from(B_CNL, bipartite=1)
        #mapping to small integers with the same sequence
        # because bipartite matching in scipy can not deal with big integers.
        normal=[]
        for mod in A_CNL:
            for vac in B_CNL:
                normal.append((abs(mod.pointer-vac.pointer), mod, vac))
        normal.sort(key=lambda elem:elem[0])
        # Add edges with weights
        mapped_weight = 0
        previous_weight = 0
        for pair in normal:
            if previous_weight != pair[0]:
                previous_weight = pair[0]
                mapped_weight += 1
            Bipartite_Graph.add_edge(pair[1], pair[2], weight= mapped_weight)
        # Obtain the minimum weight full matching
        my_matching = nx.algorithms.bipartite.matching.minimum_weight_full_matching(Bipartite_Graph, B_CNL, "weight")

        for vac in B_CNL:
            if vac in my_matching.keys():
                globals()['cnl_csg' + str(self.j)] = AnyNode(ID=self.j, name='csg' + str(self.j), parent=start_csg, Match=(my_matching[vac].ID, vac.ID))
                self.j += 1

        #For the already matched CNL, the next level is matched.
        for child in start_csg.children:
            self.POINTER_pair(child)

    def Virtual_roots(self, printer=True):

        A_index_lef=list(range(self.n))
        B_index_lef=list(range(self.n))

        while len(A_index_lef)!=0:

            globals()['cnl_A_vrm'+str(self.n+self.vrm_i)]=AnyNode(name='A_vrm'+str(self.n+self.vrm_i), ID=self.n+self.vrm_i, CNL=[], pointer=[], parent_C=None)
            globals()['cnl_B_vrm'+str(self.n+self.vrm_i)]=AnyNode(name='B_vrm'+str(self.n+self.vrm_i), ID=self.n+self.vrm_i, CNL=[], pointer=[], parent_C=None)
            #For different connected components in the configuration, design a virtual ground for their root modules to suck up.
            for index in A_index_lef:
                if self.A.nodes[index].parent==None or self.A.nodes[index].parent.ID not in A_index_lef:
                    self.A.nodes[index].parent=globals()['cnl_A_vrm'+str(self.n+self.vrm_i)]
                    globals()['cnl_A_vrm' + str(self.n+self.vrm_i)].CNL.append(sum(self.A.nodes[index].CNL)+1)
                    self.A.nodes[index].parent_C=len(globals()['cnl_A_vrm' + str(self.n+self.vrm_i)].CNL)-1

            for index in B_index_lef:
                if self.B.nodes[index].parent==None or self.B.nodes[index].parent.ID not in B_index_lef:
                    self.B.nodes[index].parent=globals()['cnl_B_vrm'+str(self.n+self.vrm_i)]
                    globals()['cnl_B_vrm' + str(self.n+self.vrm_i)].CNL.append(sum(self.B.nodes[index].CNL)+1)
                    self.B.nodes[index].parent_C=len(globals()['cnl_B_vrm' + str(self.n+self.vrm_i)].CNL)-1
            #The nodes of the virtual ground are placed at the end.
            self.A.nodes.append(globals()['cnl_A_vrm'+str(self.n+self.vrm_i)])
            self.B.nodes.append(globals()['cnl_B_vrm'+str(self.n+self.vrm_i)])
            #One-to-one pairing of newly added virtual ground
            globals()['cnl_csg' + str(self.n +self.vrm_i)] = AnyNode(ID=self.n +self.vrm_i, name='csg' + str(self.n +self.vrm_i), Match=(self.n+self.vrm_i, self.n+self.vrm_i))
            self.virtual_grounds.append(self.n+self.vrm_i)
            #The match of the virtual ground is used as the starting node of the next CNL_match.
            self.POINTER_pair(globals()['cnl_csg' + str(self.n +self.vrm_i)])
            if printer==True:
                print(RenderTree(globals()['cnl_csg' + str(self.n +self.vrm_i)]))
            self.vrm_i += 1

            A_index_del = [node.Match[0] for node in PreOrderIter(globals()['cnl_csg' + str(self.virtual_grounds[-1])])]
            B_index_del = [node.Match[1] for node in PreOrderIter(globals()['cnl_csg' + str(self.virtual_grounds[-1])])]
            A_index_lef = (set(A_index_lef).difference(set(A_index_del)))
            B_index_lef = (set(B_index_lef).difference(set(B_index_del)))
        #Save all matches except virtual grounds.
        for i in range(self.n):
            self.csg.append(globals()['cnl_csg' + str(i)])

    def Difference(self, printer=True):
        #Sort the ID numbers in the final configuration according to the new match.
        seqbak=[]
        for c in range(len(self.csg)):
            seqbak.append(self.csg[c].Match)


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






