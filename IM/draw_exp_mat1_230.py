import pickle
import matplotlib.pyplot as plt

num=230

error_cm=[]
times_cm=[]

for i in range(3,num):
    data_input = open('../../../data/results/Greedy_CM/'+str(i)+'.txt', 'rb')
    result_cm=pickle.load(data_input)
    data_input.close()

    error_cm.append(result_cm[0])
    times_cm.append(result_cm[1])

error_perm=[]
times_perm=[]

for i in range(3,num):
    data_input = open('../../../data/results/local_procrustes/'+str(i)+'.txt', 'rb')
    result_perm=pickle.load(data_input)
    data_input.close()

    error_perm.append(result_perm[0])
    times_perm.append(result_perm[1])


error_exp=[]
times_exp=[]

for i in range(3,36):
    data_input = open('../../../data/results/EXP_Pairing/'+str(i)+'.txt', 'rb')
    result_exp=pickle.load(data_input)
    data_input.close()

    error_exp.append(result_exp[0])
    times_exp.append(result_exp[1])


error_further=error_exp[:]
times_further=times_exp[:]

for i in range(36,138):
    data_input = open('../../../data/results/EXP_Pairing/further_optim_'+str(i)+'.txt', 'rb')
    result_further=pickle.load(data_input)
    data_input.close()

    error_further.append(result_further)
    times_further.append(result_further)

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
plt.plot(error_cm, color="m", label="(2) Greedy-CM")
plt.plot(error_con, color="g", label="(3) Modified Greedy-CM")
plt.plot(error_cnl, color="b", label="(4) IM (ours)")
plt.plot(error_further, color="yellow", label="(5) Further-optimized")
plt.plot(error_exp, color="black", label="(6) Optimal")
plt.xlabel('Total number of modules')
plt.ylabel('Reconfiguration steps')
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
plt.savefig('../../../data/results/error_mat1.png')

plt.show()





