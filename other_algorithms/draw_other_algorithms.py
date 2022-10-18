import pickle
import matplotlib.pyplot as plt

data_input = open('/data/results/Genetic_Algorithm/GA.txt', 'rb')
result_GA=pickle.load(data_input)
data_input.close()

error_GA=[]
times_GA=[]

for i in range(4, 141):
    error_GA.append(result_GA[i][1])
    times_GA.append(result_GA[i][2])

error_local=[]
times_local=[]

for i in range(4,141):
    data_input = open('/data/results/local_procrustes/'+str(i)+'.txt', 'rb')
    result_perm=pickle.load(data_input)
    data_input.close()

    error_local.append(result_perm[0])
    times_local.append(result_perm[1])

error_soft=[]
times_soft=[]

for i in range(4,141):
    data_input = open('/data/results/softassign/'+str(i)+'.txt', 'rb')
    result_soft=pickle.load(data_input)
    data_input.close()

    error_soft.append(result_soft[0])
    times_soft.append(result_soft[1])

plt.figure(1)
plt.plot(error_GA, color="m", label="genetic algorithm")
plt.plot(error_local, color="r", label="local-procrustes")
plt.plot(error_soft, color="c", label="softassign")
plt.xlabel('Total number of modules')
plt.ylabel('Reconfiguration steps')
#plt.title('Reconfiguration steps versus number of modules')
plt.legend(loc='upper left', bbox_to_anchor=(0.2, 0.95))
plt.savefig('/results/error_other_algorithms.png')

plt.figure(2)
plt.plot(times_GA, color="m", label="genetic algorithm")
plt.plot(times_local, color="r", label="local-procrustes")
plt.plot(times_soft, color="c", label="softassign")
plt.legend(loc='upper left', bbox_to_anchor=(0.2, 0.95))
plt.xlabel('Total number of modules')
plt.ylabel('Seconds')
#plt.title('Computational time versus number of modules')
plt.savefig('/results/times_other_algorithms.png')

#plt.show()





