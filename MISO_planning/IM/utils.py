import numpy as np
from numpy import random
import copy

def Matrix_gen(n):
    #Generate a random matrix that meets the conditions for simulating the configuration composed of MISO modules
    MI_limit=6#Limit on the number of passive connection points
    col_list=list(range(0, n+1))#One more n, used to represent the root module
    MI_limit_counts=[0]*(n+1)

    I = np.zeros((n,n))
    for i in range(n):
        finished=False
        while finished==False:
            col_list_minus=copy.deepcopy(col_list)
            # 'j!=i' means that i cannot connect to itself.
            if MI_limit_counts[i] < MI_limit:
                col_list_minus.remove(i)
            # 'j!=k' means that i cannot connect to its children
            if np.linalg.norm(I[:,i])!= 0:
                for k in range(n):
                    if I[k,i]==1 and MI_limit_counts[k] < MI_limit:
                        col_list_minus.remove(k)
            j=random.choice(col_list_minus)
            if MI_limit_counts[j]<MI_limit:
                MI_limit_counts[j]=MI_limit_counts[j]+1
                # When j==n is randomly selected, the j-th row represents the root module.
                if j != n:
                    I[i][j] = 1
                finished=True
            else:
                col_list.remove(j)

    return I

def Matrix_gen_tree(n):
    #Generate a random matrix that meets the conditions for simulating the configuration composed of MISO modules
    MI_limit=6#Limit on the number of passive connection points
    MI_limit_counts=[0]*n
    col_list=list(range(n))

    inner_tree=[]

    root= random.choice(col_list)
    col_list.remove(root)
    inner_tree.append(root)

    I = np.zeros((n,n))
    while len(inner_tree)<n:
        i=random.choice(col_list)
        j=random.choice(inner_tree)
        if MI_limit_counts[j]<MI_limit:
            MI_limit_counts[j]=MI_limit_counts[j]+1
            I[i][j] = 1
            col_list.remove(i)
            inner_tree.append(i)
    return I

def Matrix_gen_B(n, b):
    #Generate a random matrix that meets the conditions for simulating the configuration composed of MISO modules
    MI_limit=[1]*(n+1)
    for i in random.choice(n+1, b, replace=False):
        MI_limit[i]=6#Limit on the number of passive connection points
    col_list=list(range(0, n+1))#One more n, used to represent the root module
    MI_count=[0]*(n+1)

    I = np.zeros((n,n))
    for i in range(n):
        finished=False
        while finished==False:
            col_list_minus=copy.deepcopy(col_list)
            # 'j!=i' means that i cannot connect to itself.
            #Because col_list will decrease with iteration, the remaining values meet the condition of <limit.
            if MI_count[i] < MI_limit[i]:
                col_list_minus.remove(i)
            # 'j!=k' means that i cannot connect to its children
            if np.linalg.norm(I[:,i])!= 0:
                for k in range(n):
                    if I[k,i]==1 and MI_count[k] < MI_limit[k]:
                        col_list_minus.remove(k)
            j=random.choice(col_list_minus)
            if MI_count[j]<MI_limit[j]:
                MI_count[j]=MI_count[j]+1
                # When j==n is randomly selected, the j-th row represents the root module.
                if j != n:
                    I[i][j] = 1
                finished=True
            else:
                col_list.remove(j)
    return I

def Matrix_gen_B_explicit(n, b):
    #Generate a random matrix that meets the conditions for simulating the configuration composed of MISO modules
    if b>(n-2)/2:
        print('error, the number of bifurcation modules can not bigger than (n-2)/2')
    MI_limit=[1]*(n+1)
    Bifurcation_index=random.choice(n, b, replace=False)
    for i in Bifurcation_index:
        MI_limit[i]=2#Limit on the number of passive connection points
    new_assign=random.randint(min(n-2*b, (6-2)*b))

    Bifurcation_index_minus=list(copy.deepcopy(Bifurcation_index))
    i=0
    while i <= new_assign:
        # this 'choice' may contains repeated numbers
        assign=random.choice(Bifurcation_index_minus)
        if MI_limit[assign] < 6:
            MI_limit[assign] += 1
            i += 1
        else:
            Bifurcation_index_minus.remove(assign)

    col_list=list(range(0, n+1))#One more n, used to represent the root module
    one=list(set(list(range(0, n)))-set(Bifurcation_index))
    for i in random.choice(one, b+new_assign, replace=False):
        MI_limit[i]=0
        col_list.remove(i)

    MI_count=[0]*(n+1)

    I = np.zeros((n,n))
    for i in range(n):
        finished=False
        while finished==False:
            col_list_minus=copy.deepcopy(col_list)
            # 'j!=i' means that i cannot connect to itself.
            #Because col_list will decrease with iteration, the remaining values meet the condition of <limit.
            if MI_count[i] < MI_limit[i]:
                col_list_minus.remove(i)
            # 'j!=k' means that i cannot connect to its children
            if np.linalg.norm(I[:,i])!= 0:
                for k in range(n):
                    if I[k,i]==1 and MI_count[k] < MI_limit[k]:
                        col_list_minus.remove(k)
            j=random.choice(col_list_minus)
            if MI_count[j]<MI_limit[j]:
                MI_count[j]=MI_count[j]+1
                # When j==n is randomly selected, the j-th row represents the root module.
                if j != n:
                    I[i][j] = 1
                finished=True
            else:
                col_list.remove(j)
    return I

def Test_IF():

    n=12

    I = np.zeros((n,n))
    F = np.zeros((n,n))

    I[1][0]=1
    I[2][1]=1
    I[3][2]=1
    I[4][0]=1
    I[5][1]=1
    I[6][2]=1
    I[7][3]=1
    I[8][1]=1
    I[9][2]=1
    I[10][8]=1
    I[11][9]=1

    F[1][0]=1
    F[2][1]=1
    F[3][2]=1
    F[4][0]=1
    F[5][1]=1
    F[6][2]=1
    F[7][3]=1
    F[8][0]=1
    F[9][3]=1
    F[10][8]=1
    F[11][9]=1

    return I, F

def Test_IF_500():
    I=np.identity(500)
    for i in range(1, 500):
        I[-i,:]=I[-(i+1)]
    I[0,:]=0
    I[1,:]=0
    I[1, 0]=1
    I[27, :]=0
    I[27, 0]=1
    I[103, :]=0
    I[103, 0]=1
    I[173, :]=0
    I[173, 0]=1
    I[247,:]=0
    I[247,172]=1
    I[329,:]=0
    I[329,172]=1
    I[399,:]=0
    I[399,102]=1
    I[419,:]=0
    I[419,102]=1
    I[440,:]=0
    I[440,102]=1
    I[460,:]=0
    I[460,102]=1
    I[480,:]=0
    I[480,102]=1

    F=np.identity(500)
    for i in range(1, 500):
        F[-i,:]=F[-(i+1)]
    F[0,:]=0
    F[0,388]=1
    F[1,:]=0
    F[1, 0]=1
    F[52, :]=0
    F[52, 0]=1
    F[152, :]=0
    F[152, 0]=1
    F[203, :]=0
    F[203, 151]=1
    F[256, :]=0
    F[256, 151]=1
    F[304, :]=0
    F[304, 255]=1
    F[336, :]=0
    F[336, 255]=1
    F[389, :]=0
    F[389, 335]=1
    F[461, :]=0
    F[461, 335]=1

    return I, F


def hand_I_500():
    I=np.identity(500)
    for i in range(1, 500):
        I[-i,:]=I[-(i+1)]
    I[0,:]=0
    I[100,:]=0
    I[200,:]=0
    I[300,:]=0
    I[400,:]=0

    return I


def hand_F_500():
    F = np.identity(500)
    for i in range(1, 500):
        F[-i, :] = F[-(i + 1)]
    F[0, :] = 0
    F[20, :] = 0
    F[20, 0] = 1
    F[48, :] = 0
    F[48, 1] = 1
    F[76, :] = 0
    F[76, 2] = 1
    F[104, :] = 0
    F[104, 3] = 1
    F[118, :] = 0
    F[118, 4] = 1
    F[132, :] = 0
    F[132, 5] = 1
    F[146, :] = 0
    F[146, 6] = 1
    F[176, :] = 0
    F[176, 7] = 1
    F[206, :] = 0
    F[206, 8] = 1
    F[236, :] = 0
    F[236, 9] = 1
    F[250, :] = 0
    F[250, 10] = 1
    F[264, :] = 0
    F[264, 11] = 1
    F[293, :] = 0
    F[293, 12] = 1
    F[322, :] = 0
    F[322, 13] = 1
    F[351, :] = 0
    F[351, 14] = 1
    F[365, :] = 0
    F[365, 15] = 1
    F[379, :] = 0
    F[379, 16] = 1
    F[393, :] = 0
    F[393, 17] = 1
    F[418, :] = 0
    F[418, 18] = 1
    F[443, :] = 0
    F[443, 19] = 1
    F[468, :] = 0
    F[468, 28] = 1
    F[479, :] = 0
    F[479, 29] = 1
    F[490, :] = 0
    F[490, 55] = 1

    return F

def human_F_568():
    F = np.identity(568)
    for i in range(1, 568):
        F[-i, :] = F[-(i + 1)]
    F[0, :] = 0

    new=[]
    new.append([18,0])
    new.append([20,0])
    new.append([23,1])
    new.append([25,1])
    new.append([28,2])
    new.append([30,2])
    new.append([33,3])
    new.append([35,3])
    new.append([38,4])
    new.append([47,4])
    new.append([57,5])
    new.append([65,5])
    new.append([74,64])
    new.append([90,64])
    new.append([105,73])
    new.append([121,73])
    new.append([136,6])
    new.append([144,6])
    new.append([153,143])
    new.append([169,143])
    new.append([184,152])
    new.append([200,152])
    new.append([215,7])
    new.append([224,7])
    new.append([234,8])
    new.append([243,8])
    new.append([253,9])
    new.append([262,9])
    new.append([272,10])
    new.append([281,10])
    new.append([291,11])
    new.append([300,11])
    new.append([310,12])
    new.append([319,12])
    new.append([329,13])
    new.append([338,13])
    new.append([348,14])
    new.append([357,14])
    new.append([367,15])
    new.append([376,15])
    new.append([386,16])
    new.append([395,16])
    new.append([405,17])
    new.append([414,408])
    new.append([432,409])
    new.append([450,410])
    new.append([468,411])
    new.append([486,17])
    new.append([496,490])
    new.append([514,491])
    new.append([532,492])
    new.append([550,493])
    
    for n in new:
        F[n[0],:]=0
        F[n[0],n[1]]=1
    return F

def human_I_568():
    I=np.identity(568)
    for i in range(1, 568):
        I[-i,:]=I[-(i+1)]
    I[0,:]=0
    I[100,:]=0
    I[200,:]=0
    I[300,:]=0
    I[400,:]=0
    I[500,:]=0

    return I

