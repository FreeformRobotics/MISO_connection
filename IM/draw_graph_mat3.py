import pickle
import matplotlib.pyplot as plt

error_con=[]
times_con=[]
N=489
for i in range(3,N):
    data_input = open('../../../data/results/CON_Pairing/Matrix3_'+str(i)+'.txt', 'rb')
    result_con=pickle.load(data_input)
    data_input.close()

    error_con.append(result_con[0])
    times_con.append(result_con[1])

error_cnl=[]
times_cnl=[]

for i in range(3,N):
    data_input = open('../../../data/results/CNL_Pairing/Matrix3_'+str(i)+'.txt', 'rb')
    result_cnl=pickle.load(data_input)
    data_input.close()

    error_cnl.append(result_cnl[0])
    times_cnl.append(result_cnl[1])


plt.figure(1)
plt.plot(error_con, color="g", label="(1) Modified Greedy-CM")
plt.plot(error_cnl, color="b", label="(2) IM (ours)")
plt.xlabel('Exact number of bifurcation modules')
plt.ylabel('Reconfiguration steps')
plt.legend(loc='upper left', bbox_to_anchor=(0.52, 0.99))
plt.savefig('../../../data/results/error_mat3.png')

plt.figure(2)
plt.plot(times_con, color="g", label="Modified Greedy-CM")
plt.plot(times_cnl, color="b", label="IM (ours)")
plt.legend(loc='upper left', bbox_to_anchor=(0.01, 0.96))
plt.xlabel('Exact number of bifurcation modules')
plt.ylabel('Seconds')
plt.savefig('../../../data/results/times_mat3.png')

plt.show()





