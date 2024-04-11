import numpy as np
from anytree import AnyNode, RenderTree
import itertools
import pickle
import copy
import os

class EXP_Pairing():
    def __init__(self, A, B, IM_bound):
        self.A=A
        self.B=B
        self.n =np.shape(A.matrix)[0]
        self.best_match=[]
        self.further_num=0

        self.num_nodes=self.n
        #num_nodes represents the number of nodes in the psudo-tree
        self.UPPER=IM_bound
        self.LOWER=self.lower_bound(printer=False)
        #Take the near-optimal solution of the IM algorithm as the upper bound.

    def cal_cost(self, module_a, mask_a, module_b, mask_b):
        cost=0
        A_parent=0
        if self.A.nodes[module_a].parent != None and self.A.nodes[module_a].parent.ID not in mask_a:
            A_parent = 1
            #If the parent module exists and is not matched
        B_parent=0
        if self.B.nodes[module_b].parent != None and self.B.nodes[module_b].parent.ID not in mask_b:
            B_parent = 1
        A_child = []
        for child in self.A.nodes[module_a].children:
            if child.ID not in mask_a:
                #Delete child modules that have been matched
                A_child.append(child.ID)
        B_child = []
        for child in self.B.nodes[module_b].children:
            if child.ID not in mask_b:
                B_child.append(child.ID)
        cost += abs(A_parent-B_parent)+abs(len(A_child) - len(B_child))
        #The cost is defined by the absolute difference between the number of child-modules and parent-modules
        return cost, A_child, B_child

    def generate(self, parent_node_ID, printer=True):
        parent_node=globals()['exp_' + str(parent_node_ID)]
        Matches = parent_node.Matches

        if len(parent_node.mask_a) == self.n:
            #All matches are complete.
            self.UPPER = parent_node.cost
            #update upper bound
            self.best_match=[(parent_node.mask_a[i], parent_node.mask_b[i]) for i in range(self.n)]
            #Save matching results.
            self.further_num += 1
            data_output = open(os.path.join(os.path.dirname(__file__), 'results/further_optim_'+ str(self.further_num)+'.txt'), 'wb')
            pickle.dump(self.best_match, data_output)
            data_output.close()
            print('n:{}; further_num:{}; UPPER:{}'.format(self.n, self.further_num, self.UPPER))
            return

        if len(parent_node.mask_a)!=self.n and Matches==[]:
            #Not yet matched completely, but has reached the end of the subtree.
            roots_a=[]#only select one root, an improvement can be maken by removing some root modules with CN<2
            for i in set(range(self.n))-set(parent_node.mask_a):
                if self.A.nodes[i].parent== None or self.A.nodes[i].parent.ID in parent_node.mask_a:
                    roots_a.append(i)

            vacancies_b=set(range(self.n))-set(parent_node.mask_b)

            for vacancy in vacancies_b:
                cost_current = parent_node.cost

                cost, _, _ = self.cal_cost(roots_a[0], parent_node.mask_a, vacancy, parent_node.mask_b)
                cost_current += cost
                if cost_current < self.UPPER:
                    globals()['exp_' + str(self.num_nodes)] = AnyNode(ID=self.num_nodes, name='exp_' + str(self.num_nodes), \
                                                                      parent=parent_node, \
                                                                      Matches=parent_node.Matches+[(roots_a[0], vacancy)], cost=cost_current, \
                                                                      mask_a=parent_node.mask_a + [roots_a[0]], \
                                                                      mask_b=parent_node.mask_b + [vacancy])

                    self.OPEN.append(self.num_nodes)
                    self.num_nodes += 1
            if printer==True:
                print(RenderTree(parent_node))
                #print('len(self.OPEN):{}'.format(len(self.OPEN)))
                print('re-assigned')
            return

        match_perm_all_parent = []
        #All possible permutations between the children of a module and a vacancy in each match
        for Match in Matches:
            #Matches in each node hold several matches. Each match contains a module and vacancy in the initial and final configuration.
            _, A_child, B_child=self.cal_cost(Match[0], parent_node.mask_a, Match[1], parent_node.mask_b)
            #Count the number of children of a module and a vacancy in a match.
            match_perm_one_parent = []
            match_init=[]
            for a_child in reversed(A_child):
                #"reversed" is for "romove" to avoid destroying the traversability of the "for" loop
                if all([CN<=2 for CN in self.A.nodes[a_child].CNL])==True:
                    #If all CNs in the CNL are not greater than 2, it is optimal that the two CNLs can be directly matched when they are equal.
                    for b_child in reversed(B_child):
                        if self.A.nodes[a_child].CNL==self.B.nodes[b_child].CNL:
                            #This direct matching can reduce the number of subsequent permutations
                            match_init.append((a_child, b_child))
                            A_child.remove(a_child)
                            B_child.remove(b_child)
                            break
            #All possible permutations between the children of a module and a vacancy in a match
            if len(A_child) >= len(B_child):
                for Aperm in itertools.permutations(A_child, len(B_child)):
                    match_perm = copy.copy(match_init)
                    #One permutation between the children of a module and a vacancy in a match
                    cost_current = parent_node.cost
                    #The initial value of the current cost is the cost of the parent node.
                    for i in range(len(B_child)):
                        #Calculate the total cost for each permutation.
                        match_perm.append((Aperm[i], B_child[i]))
                        cost, _, _=self.cal_cost(Aperm[i], parent_node.mask_a, B_child[i], parent_node.mask_b)
                        #The cost of one new match in the permutation
                        cost_current += cost
                        if cost_current >= self.UPPER:
                            break
                            # It has exceeded the upper bound before the accumulation is complete.
                    if cost_current < self.UPPER:
                        match_perm.append(cost_current)
                        #If the current cost is less than the upper bound, the cost is appended to match_perm for further use.
                        match_perm_one_parent.append(match_perm)
                        #Save one permutation.
            else:
                for Bperm in itertools.permutations(B_child, len(A_child)):
                    match_perm = copy.copy(match_init)
                    cost_current = parent_node.cost
                    for i in range(len(A_child)):
                        match_perm.append((A_child[i], Bperm[i]))
                        cost, _, _=self.cal_cost(A_child[i], parent_node.mask_a, Bperm[i], parent_node.mask_b)
                        cost_current += cost
                        if cost_current >= self.UPPER:
                            break
                            # It has exceeded the upper bound before the accumulation is complete.
                    if cost_current < self.UPPER:
                        match_perm.append(cost_current)
                        match_perm_one_parent.append(match_perm)
            match_perm_all_parent.append(match_perm_one_parent)
            #After the for loop ends, match_perm_one_parent contains all match_perm. and then match_perm_one_parent is appended to match_perm_all_parent

        while len(match_perm_all_parent) > 1:
            #Each row in match_perm_all_parent is fully arranged to merge into one row.
            A_one_parent = match_perm_all_parent.pop()
            B_one_parent = match_perm_all_parent.pop()
            second_perm_one_parent = []
            for A_match_perm in A_one_parent:
                for B_match_perm in B_one_parent:
                    #Match any two of the two lines in match_perm_all_parent
                    second_cost = A_match_perm[-1] + B_match_perm[-1] - parent_node.cost
                    #The costs are added but the repeated initial cost is subtracted.
                    if second_cost < self.UPPER:
                        #Only permutations smaller than the upper bound are useful
                        second_perm = A_match_perm[0:-1] + B_match_perm[0:-1]
                        second_perm.append(second_cost)
                        second_perm_one_parent.append(second_perm)
                        #Possible permutations of two lines in match_perm_all_parent
            match_perm_all_parent.append(second_perm_one_parent)
            #The merged new line is re-entered

        for last_perm in match_perm_all_parent[0]:
            #match_perm_all_parent only has one line left at the end.
            globals()['exp_' + str(self.num_nodes)] = AnyNode(ID=self.num_nodes, name='exp_' + str(self.num_nodes), \
                                                              parent=parent_node, \
                                                              Matches=last_perm[0:-1], cost=last_perm[-1], \
                                                              mask_a=parent_node.mask_a+[last_perm[i][0] for i in range(len(last_perm)-1)], \
                                                              mask_b=parent_node.mask_b+[last_perm[i][1] for i in range(len(last_perm)-1)])
            self.OPEN.append(self.num_nodes)
            self.num_nodes += 1
        if printer==True:
            print(RenderTree(parent_node))
        #print('len(self.OPEN):{}'.format(len(self.OPEN)))

    def EXP_pairing(self, printer=True):
        self.OPEN=[]
        #OPEN store nodes need to be tested.

        for vacancy in range(self.B.matrix.shape[0]):
            cost_current=0
            cost, _, _ = self.cal_cost(self.A.roots[0], [], vacancy, [])
            cost_current += cost
            if cost_current < self.UPPER:
                globals()['exp_' + str(self.num_nodes)] = AnyNode(ID=self.num_nodes, name='exp_' + str(self.num_nodes), \
                                                                  parent=None, Matches=[(self.A.roots[0], vacancy)], cost=cost_current, \
                                                                  mask_a=[self.A.roots[0]], mask_b=[vacancy])
                self.OPEN.append(self.num_nodes)
                self.num_nodes += 1

        #label correcting algorithm
        while self.OPEN!=[] and self.UPPER > self.LOWER:
                parent_node_ID=self.OPEN.pop()
                self.generate(parent_node_ID, printer)
        print('One optimal solution is reached: {}. '.format(self.UPPER))

    def Difference(self, printer=True):
        #Sort the ID numbers in the final configuration according to the new match.
        if self.best_match==[]:
            return 'the same with IM', self.UPPER
        seqbak=[]
        for i in range(len(self.best_match)):
            seqbak.append(self.best_match[i])

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





