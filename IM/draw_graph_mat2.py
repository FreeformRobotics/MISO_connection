import pickle
import matplotlib.pyplot as plt

error_con=[]
times_con=[]

for i in range(3,1000):
    data_input = open('../../../data/results/CON_Pairing/Matrix2_'+str(i)+'.txt', 'rb')
    result_con=pickle.load(data_input)
    data_input.close()

    error_con.append(result_con[0])
    times_con.append(result_con[1])

error_cnl=[]
times_cnl=[]

for i in range(3,1000):
    data_input = open('../../../data/results/CNL_Pairing/Matrix2_'+str(i)+'.txt', 'rb')
    result_cnl=pickle.load(data_input)
    data_input.close()

    error_cnl.append(result_cnl[0])
    times_cnl.append(result_cnl[1])


plt.figure(1)
plt.plot(error_con, color="g", label="(1) Modified Greedy-CM")
plt.plot(error_cnl, color="b", label="(2) IM (ours)")
plt.xlabel('Upper bound of the number of bifurcation modules')
plt.ylabel('Reconfiguration steps')
plt.legend(loc='upper left', bbox_to_anchor=(0.09, 0.99))
plt.savefig('../../../data/results/error_mat2.png')

plt.figure(2)
plt.plot(times_con, color="g", label="Modified Greedy-CM")
plt.plot(times_cnl, color="b", label="IM (ours)")
plt.legend(loc='upper left', bbox_to_anchor=(0.09, 0.99))
plt.xlabel('Upper bound of the number of bifurcation modules')
plt.ylabel('Seconds')
plt.savefig('../../../data/results/times_mat2.png')

#plt.show()





