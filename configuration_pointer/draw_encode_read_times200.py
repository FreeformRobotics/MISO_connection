import pickle
import matplotlib.pyplot as plt

N=200

data_input = open('/data/results/encode_times200.txt', 'rb')
encode_times=pickle.load(data_input)
data_input.close()

data_input = open('/data/results/read_times200.txt', 'rb')
read_times=pickle.load(data_input)
data_input.close()



plt.figure(1)
plt.plot(encode_times, color="olive", label="encoding times")
plt.plot(read_times, color="brown", label="reading times")
plt.xlabel('Number of Experiments')
plt.ylabel('Seconds')
plt.legend(loc='upper left', bbox_to_anchor=(0.01, 0.99))
plt.savefig('/results/read_encode_times200.png')

#
plt.show()





