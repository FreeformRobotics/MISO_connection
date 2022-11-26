import numpy as np
from anytree import AnyNode, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source
from collections import defaultdict

class Matrix2tree():
    def __init__(self, Matrix, Name):
        self.matrix=Matrix
        self.name=Name
        #Indices of all vertices, the corresponding index will be deleted from this list whenever a new node is created.
        self.allV = list(range(np.shape(Matrix)[0]))
        #Save the indices of the root modules
        self.roots=[]
        self.disconnect=[]
        self.MI_limit = 6
        #Save all the nodes created
        self.nodes = []

    def loop_tree(self, parent_ID):
        #Create child nodes based on the ID of the parent node
        child_list=[index for (index, value) in enumerate(list(self.matrix[:, parent_ID])) if value == 1]
        if len(child_list)!=0:
            for child in child_list:
                #CNL is initialized to 0
                globals()['v' + str(parent_ID)].CNL.append(0)
                self.allV.remove(child)
                globals()['v' + str(child)] = AnyNode(name='v' + str(child), parent=globals()['v' + str(parent_ID)], ID=child, CNL=[], pointer=[], parent_C=None, pose=[], robot=None)
                self.loop_tree(child)

    def matrix2tree(self, printer=True):
        if printer==True:
            print("{} configuration".format(self.name))
        for i in range(np.shape(self.matrix)[0]):
            #The line with all zeros is the root module
            if np.linalg.norm(self.matrix[i,:])==0:
                self.roots.append(i)
                self.allV.remove(i)
                globals()['v'+str(i)]=AnyNode(name='v'+str(i), ID=i, CNL=[], pointer=[], parent_C=None, pose=[], robot=None)
                self.loop_tree(i)

        #The remaining nodes form multiple circuits.
        while len(self.allV)!=0:
            circuit=[]
            #Starting from any node in the circuit and moving in the direction of the parent node, it will eventually converge to the cycle in the circuit.
            circuit.append(self.allV[0])
            j=list(self.matrix[self.allV[0],:]).index(1)
            while j not in circuit:
                circuit.append(j)
                j = list(self.matrix[j,:]).index(1)
            else:
                if printer==True:
                    print('the length of cycle in the circuit:{}'.format(len(circuit)-circuit.index(j)))
                #When a node that has appeared in circuit is detected, it means that the cycle has been traversed.
                self.roots.append(j)
                self.allV.remove(j)
                #It can be disconnected at any node of the cycle.
                if printer==True:
                    print('{} Matrix disconnect ({},{})'.format(self.name, j, list(self.matrix[j, :]).index(1)))
                self.disconnect.append((j, list(self.matrix[j, :]).index(1)))
                self.matrix[j,:]=0
                globals()['v'+str(j)]=AnyNode(name='v'+str(j), ID=j, CNL=[], pointer=[], parent_C=None, pose=[], robot=None)
                self.loop_tree(j)

    def CNL_cal(self):
        for root in self.roots:
            for leaf in globals()['v' + str(root)].leaves:
                leaf.CNL.append(0)
                #To calculate CNL, go up from the leaf node of a tree
                branch_sum=0
                for i in range(2, len(leaf.path)+1):
                    if leaf.path[-i+1].parent_C==None:
                        leaf.path[-i+1].parent_C=leaf.path[-i].CNL.index(0)
                        #Choose a CN and increase it in the direction of the parent node.
                        leaf.path[-i].CNL[leaf.path[-i+1].parent_C] += i-1
                        branch_sum=i-1
                    else:
                        #If encounter a module that has been assigned parent_C in other leaf.path, CN will not be increased but just add branch_sum.
                        leaf.path[-i].CNL[leaf.path[-i + 1].parent_C] += branch_sum

    def tree_render(self,printer=True, draw=False):
        for root in self.roots:
            if printer==True:
                print(RenderTree(globals()['v'+str(root)]))
            if draw==True:
                #Draw a diagram of the tree
                DotExporter(globals()['v'+str(root)]).to_dotfile("trees/{}_r{}.dot".format(self.name, root))
                src = Source.from_file('trees/{}_r{}.dot'.format(self.name, root))
                src.format = 'png'
                src.render('trees/{}_r{}'.format(self.name, root))

        #Save all the nodes created
        for i in range(np.shape(self.matrix)[0]):
            self.nodes.append(globals()['v'+str(i)])

    def Pointer(self):
        for root in self.roots:
            Bifurcation=[]
            #Bifurcation = search.findall(globals()['v' + str(root)], filter_=lambda node: len(node.CNL)>1)
            for leaf in globals()['v' + str(root)].leaves:
                leaf.pointer.append(leaf.CNL)
                for i in range(2, len(leaf.path)+1):
                    if len(leaf.path[-i].CNL)==1:
                        leaf.path[-i].pointer.append(leaf.path[-i].CNL)
                        for l in leaf.path[-i+1].pointer:
                            leaf.path[-i].pointer.append(l)
                    else:
                        Bifurcation.append(leaf.path[-i])
                        break
            Bifurcation=list(set(Bifurcation))

            while len(Bifurcation)!=0:
                for B in Bifurcation:
                    Active=True
                    for child in B.children:
                        if child.pointer==[]:
                            Active=False
                    if Active==True:
                        B.pointer.append(sorted(B.CNL, reverse=True))

                        def list_duplicates(seq):
                            tally = defaultdict(list)
                            for i, item in enumerate(seq):
                                tally[item].append(i)
                            return ((key, locs) for key, locs in tally.items())

                        for dup in sorted(list_duplicates(B.CNL), reverse=True):
                            if len(dup[1]) == 1:
                                for child in B.children:
                                    if child.parent_C == dup[1][0]:
                                        for l in child.pointer:
                                            B.pointer.append(l)
                            else:
                                Current_number = []
                                for child in B.children:
                                    if child.parent_C in dup[1]:
                                        number = ''
                                        for l in child.pointer:
                                            if l!=[0] and l != [1]:# delete '0' and '1' in pointer
                                                number = number+''.join(map(str, l))
                                        if number=='':
                                            number='0'
                                        Current_number.append((int(number), child.pointer))

                                Current_number.sort(key=lambda elem:elem[0], reverse=True)
                                for s in Current_number:
                                    for l in s[1]:
                                        B.pointer.append(l)
                        if B.parent!=None:
                            pre=B.parent
                            cur=B
                            while pre != None and len(pre.CNL)==1:
                                pre.pointer.append(pre.CNL)
                                for l in cur.pointer:
                                    pre.pointer.append(l)
                                cur=pre
                                pre=pre.parent
                            else:
                                Bifurcation.remove(B)
                                if pre != None:
                                    Bifurcation.append(pre)
                        else:
                            Bifurcation.remove(B)
                        Bifurcation=list(set(Bifurcation))
                        break

    def Pointer_int(self, printer=True):
        #pointers ready
        for node in self.nodes:
            sig = ''
            for l in node.pointer:
                if l != [0] and l != [1]:  # delete '0' and '1' in pointer
                    sig = sig+''.join((map(str, l)))
            if sig=='':
                sig='0'
            node.pointer=int(sig)
        sigs=[]
        if printer==True:
            for root in self.roots:
                print(RenderTree(globals()['v' + str(root)]))
                sigs.append(globals()['v' + str(root)].pointer)

        return sigs








