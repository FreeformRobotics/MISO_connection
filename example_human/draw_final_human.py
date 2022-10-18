import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import pickle

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

#int(np.linalg.noram(matrices1[2]-matrices[2], ord='fro') ** 2)

points_F=np.zeros((568, 2))
id=0
points_F[id,:]=[6, 12]

num=18
for i in range(id+1, num):
    points_F[i,:]=[points_F[i-1, 0], points_F[i-1, 1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

for head in range(4):
    points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*head]
    num=2
    for i in range(id+1, id + num):
        points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
    id += num
    plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

    points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*head]
    num=3
    for i in range(id+1, id + num):
        points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
    id += num
    plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

body_n=4
points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*body_n]
num=9
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*body_n]
num=10
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

body_n=5
points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*body_n]
num=8
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*body_n]
num=9
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left arm 1
points_F[id,:]=[points_F[64, 0]-0.24, points_F[64, 1]+0.06]
num=16
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[64, 0]-0.24, points_F[64, 1]-0.06]
num=15
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right arm 1
points_F[id,:]=[points_F[73, 0]+0.24, points_F[73, 1]+0.06]
num=16
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[73, 0]+0.24, points_F[73, 1]-0.06]
num=15
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)


body_n=6
points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*body_n]
num=8
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*body_n]
num=9
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left arm 2
points_F[id,:]=[points_F[143, 0]-0.24, points_F[143, 1]-0.12+0.06]
num=16
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[143, 0]-0.24, points_F[143, 1]-0.12-0.06]
num=15
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right arm 2
points_F[id,:]=[points_F[152, 0]+0.24, points_F[152, 1]-0.12+0.06]
num=16
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

points_F[id,:]=[points_F[152, 0]+0.24, points_F[152, 1]-0.12-0.06]
num=15
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

for body_n in range(7,17):
    points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*body_n]
    num=9
    for i in range(id+1, id + num):
        points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
    id += num
    plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

    points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*body_n]
    num=10
    for i in range(id+1, id + num):
        points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
    id += num
    plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left leg
body_n=17
points_F[id,:]=[points_F[0, 0]-0.12, points_F[0, 1]-0.12*body_n]
num=9
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]-0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left leg 1
points_F[id,:]=[points_F[408, 0], points_F[408, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left leg 2
points_F[id,:]=[points_F[409, 0], points_F[409, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left leg 3
points_F[id,:]=[points_F[410, 0], points_F[410, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#left leg 3
points_F[id,:]=[points_F[411, 0], points_F[411, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right leg
body_n=17
points_F[id,:]=[points_F[0, 0]+0.12, points_F[0, 1]-0.12*body_n]
num=10
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0]+0.12, points_F[i-1,1]]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right leg 1
points_F[id,:]=[points_F[490, 0], points_F[490, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right leg 2
points_F[id,:]=[points_F[491, 0], points_F[491, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right leg 3
points_F[id,:]=[points_F[492, 0], points_F[492, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)

#right leg 4
points_F[id,:]=[points_F[493, 0], points_F[493, 1]-0.12]
num=18
for i in range(id+1, id + num):
    points_F[i, :]=[points_F[i-1,0], points_F[i-1,1]-0.12]
id += num
plt.plot(points_F[id-num:id, 0], points_F[id-num:id, 1], linewidth=width, color=colo)


id_IM=[]
for i in range(568):
    for j in range(568):
        if matrices[0][i, j]==1:
            id_IM.append(matrices[1][i])

id_Greedy=[]
for i in range(568):
    for j in range(568):
        if matrices1[0][i, j]==1:
            id_Greedy.append(matrices1[1][i])

id_common=set(id_IM).intersection(set(id_Greedy))
id_IM=set(id_IM).difference(set(id_common))
id_Greedy=set(id_Greedy).difference(set(id_common))

X_IM=[]
Y_IM=[]
for id in id_IM:
    X_IM.append(points_F[id, 0])
    Y_IM.append(points_F[id, 1])

X_Greedy=[]
Y_Greedy=[]
for id in id_Greedy:
    X_Greedy.append(points_F[id, 0])
    Y_Greedy.append(points_F[id, 1])

X_common=[]
Y_common=[]
for id in id_common:
    X_common.append(points_F[id, 0])
    Y_common.append(points_F[id, 1])
plt.scatter(X_common, Y_common, linewidths=width_s, color='pink', label='common')
plt.scatter(X_IM, Y_IM, linewidths=width_s, color='goldenrod', label='IM')
plt.scatter(X_Greedy, Y_Greedy, linewidths=width_s, color='saddlebrown', label='M G-CM')

plt.legend(loc='upper left', bbox_to_anchor=(0.05, 0.4))

# axes = plt.gca()
# axes.set_xlim([0,10])
# axes.set_ylim([5,13])

plt.axis('off')

plt.savefig('/results/attach_human_two.png', dpi=130)
plt.show()