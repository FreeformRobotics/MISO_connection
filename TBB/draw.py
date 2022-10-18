import pickle
import matplotlib.pyplot as plt

N=36

error_exp=[]
times_exp=[]
for i in range(4, N):
    if i==24:
        continue
    data_input = open('data/results/EXP_Pairing/mp_time_'+str(i)+'.txt', 'rb')
    result_exp=pickle.load(data_input)
    data_input.close()

    error_exp.append(result_exp[0])
    times_exp.append(result_exp[1])

error_cnl=[]
times_cnl=[]

for i in range(4, N):
    if i==24:
        continue
    data_input = open('data/results/CNL_Pairing/Matrix1_'+str(i)+'.txt', 'rb')
    result_cnl=pickle.load(data_input)
    data_input.close()

    error_cnl.append(result_cnl[0])
    times_cnl.append(result_cnl[1])


plt.figure(1)
plt.plot(error_cnl, color="b", label="Near-optimal")
plt.plot(error_exp, color="y", label="Optimal")
plt.xlabel('N')
plt.ylabel('Reconfiguration steps')
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.995))
plt.savefig('data/results/error_exp_mat1.png')

plt.figure(2)
plt.plot(times_cnl, color="b", label="Near-optimal")
plt.plot(times_exp, color="y", label="Optimal")
plt.xlabel('N')
plt.ylabel('times')
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.995))
plt.savefig('data/results/times_exp_mat1.png')


#plt.show()





