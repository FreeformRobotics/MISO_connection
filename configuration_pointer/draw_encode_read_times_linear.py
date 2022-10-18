import pickle
import matplotlib.pyplot as plt

N=240

data_input = open('/data/results/encode_times_linear.txt', 'rb')
encode_times=pickle.load(data_input)
data_input.close()

data_input = open('/data/results/read_times_linear.txt', 'rb')
read_times=pickle.load(data_input)
data_input.close()



plt.figure(1)
plt.plot(encode_times, color="olive", label="encoding time")
plt.plot(read_times, color="brown", label="reading time")
plt.xlabel('Total number of modules')
plt.ylabel('Seconds')
plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
plt.savefig('/results/read_encode_times_linear.png')


plt.show()





