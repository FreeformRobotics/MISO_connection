import pickle
import pickle
import matplotlib.pyplot as plt

num=1000


error_perm=[]
times_perm=[]

for i in range(3,num):
    data_input = open('../../../data/results/local_procrustes/'+str(i)+'.txt', 'rb')
    result_perm=pickle.load(data_input)
    data_input.close()

    error_perm.append(result_perm[0])
    times_perm.append(result_perm[1])


error_con=[]
times_con=[]

for i in range(3,num):
    data_input = open('../../../data/results/CON_Pairing/'+str(i)+'.txt', 'rb')
    result_con=pickle.load(data_input)
    data_input.close()

    error_con.append(result_con[0])
    times_con.append(result_con[1])

error_cnl=[]
times_cnl=[]

for i in range(3,num):
    data_input = open('../../../data/results/CNL_Pairing/'+str(i)+'.txt', 'rb')
    result_cnl=pickle.load(data_input)
    data_input.close()


    error_cnl.append(result_cnl[0])
    times_cnl.append(result_cnl[1])


plt.figure(1)
plt.plot(error_perm, color="r", label="(1) local-procrustes")
#plt.plot(error_cm, color="m", label="(2) Greedy-CM")
plt.plot(error_con, color="g", label="(2) Modified Greedy-CM")
plt.plot(error_cnl, color="b", label="(3) IM (ours)")
#plt.plot(error_further, color="grey", label="(5) Further-optimized")
#plt.plot(error_exp, color="black", label="(6) Optimal")
plt.xlabel('Total number of modules')
plt.ylabel('Reconfiguration steps')
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
plt.savefig('../../../data/results/error_mat1.png')

plt.figure(2)
plt.plot(times_perm, color="r", label="(1) local-procrustes")
plt.plot(times_con, color="g", label="(2) Modified Greedy-CM")
plt.plot(times_cnl, color='b', label="(3) IM (ours)")
#plt.plot(times_cm, color="m", label="Greedy-CM")
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
plt.xlabel('Total number of modules')
plt.ylabel('Seconds')
plt.savefig('../../../data/results/times_mat1.png')

plt.show()





