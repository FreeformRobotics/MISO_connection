import numpy as np
import matplotlib.pyplot as plt
import pickle
# plt.figure(figsize=())

data_input = open('/data/results/human_cnl.txt', 'rb')
matrices = pickle.load(data_input)
data_input.close()
#
data_input = open('/data/results/human_con.txt', 'rb')
matrices1 = pickle.load(data_input)
data_input.close()

width=2.5
width_s=3.5
colo=(70/255, 114/255, 196/255)
colo_green=(0, 176/255, 80/255)
colo_red=(1, 0, 0)


#int(np.linalg.norm(matrices1[2]-matrices[2], ord='fro') ** 2)

points_I_all=np.zeros((568, 2))

def layer(init_p):
    points_I = np.zeros((100, 2))
    id=0
    points_I[id,:]=init_p
    for i in range(id+1, id + 10):
        points_I[i, :]=[points_I[i-1, 0]+0.12, points_I[i-1,1]]
    id += 10

    for hang in range(1, 10):
        points_I[id, :] = [points_I[id - 1, 0], points_I[id - 1, 1] + 0.12]
        if hang%2==0:
            margin=0.12
        else:
            margin=-0.12
        for i in range(id+1, id + 10):
            points_I[i, :]=[points_I[i-1, 0]+margin, points_I[i-1,1]]
        id += 10
    return points_I

points_I_1=layer([0, 0])
plt.plot(points_I_1[:, 0], points_I_1[:, 1], linewidth=width, color=colo)
points_I_all[0:100, :]=points_I_1

points_I_2=layer([1.5, 0])
plt.plot(points_I_2[:, 0], points_I_2[:, 1], linewidth=width, color=colo)
points_I_all[100:200, :]=points_I_2

points_I_3=layer([0, 1.3])
plt.plot(points_I_3[:, 0], points_I_3[:, 1], linewidth=width, color=colo)
points_I_all[200:300, :]=points_I_3

points_I_4=layer([1.5, 1.3])
plt.plot(points_I_4[:, 0], points_I_4[:, 1], linewidth=width, color=colo)
points_I_all[300:400, :]=points_I_4

points_I_5=layer([3, 0])
plt.plot(points_I_5[:, 0], points_I_5[:, 1], linewidth=width, color=colo)
points_I_all[400:500, :]=points_I_5

def layer_len(init_p, len):
    points_I = np.zeros((len, 2))
    id=0
    points_I[id,:]=init_p
    for i in range(id+1, id + 10):
        points_I[i, :]=[points_I[i-1, 0]+0.12, points_I[i-1,1]]
    id += 10
    for hang in range(1, 10):
        points_I[id, :] = [points_I[id - 1, 0], points_I[id - 1, 1] + 0.12]
        if hang%2==0:
            margin=0.12
        else:
            margin=-0.12
        for i in range(id+1, id + 10):
            if i==68:
                return points_I
            points_I[i, :]=[points_I[i-1, 0]+margin, points_I[i-1,1]]
        id += 10
    return points_I

points_I_6=layer_len([3, 1.3], 68)
plt.plot(points_I_6[:, 0], points_I_6[:, 1], linewidth=width, color=colo)
points_I_all[500:, :]=points_I_6


id_IM=[]
for i in range(568):
    for j in range(568):
        if matrices[0][i, j]==1:
            id_IM.append(i)

id_Greedy=[]
for i in range(568):
    for j in range(568):
        if matrices1[0][i, j]==1:
            id_Greedy.append(i)

id_common=set(id_IM).intersection(set(id_Greedy))
id_IM=set(id_IM).difference(set(id_common))
id_Greedy=set(id_Greedy).difference(set(id_common))

X_IM=[]
Y_IM=[]
for id in id_IM:
        X_IM.append(points_I_all[id, 0])
        Y_IM.append(points_I_all[id, 1])

X_Greedy=[]
Y_Greedy=[]
for id in id_Greedy:
        X_Greedy.append(points_I_all[id, 0])
        Y_Greedy.append(points_I_all[id, 1])


X_common=[]
Y_common=[]
for id in id_common:
    X_common.append(points_I_all[id, 0])
    Y_common.append(points_I_all[id, 1])

plt.scatter(X_common, Y_common, linewidths=width_s, color='pink', label='common')
plt.scatter(X_IM, Y_IM, linewidths=width_s, color='goldenrod', label='IM')
plt.scatter(X_Greedy, Y_Greedy, linewidths=width_s, color='saddlebrown', label='M G-CM')


plt.legend(loc='upper right', bbox_to_anchor=(1, 1))

axes = plt.gca()
axes.set_xlim([-0.2,4.3])
axes.set_ylim([-0.2,2.8])
plt.axis('off')


#plt.savefig('detach_human_IM.png', dpi=130)
plt.savefig('/results/detach_human_two.png', dpi=130)
# plt.show()