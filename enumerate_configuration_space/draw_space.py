import pickle
import matplotlib.pyplot as plt
import numpy as np
import math

f=open('/data/results/space_volume.txt', 'rb')
space_volume=pickle.load(f)
f.close()

space_volume_log=[]
for v in space_volume:
    space_volume_log.append(math.log(v, 2))

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(space_volume, color="teal", label="logarithmic coordinate")
ax1.set_xlabel('Total number of modules')
ax1.set_ylabel('Volume of the configuration space')

ax1.set_yscale("log")

major_ticks_log=[3,9,15,21,27,33,39]
major_ticks=[]
for i in major_ticks_log:
    major_ticks.append(float(pow(10, i)))

minor_ticks=[]
for j in np.linspace(1, major_ticks[0],10):
    minor_ticks.append(j)
for i in range(len(major_ticks)-1):
    for j in np.linspace(major_ticks[i],major_ticks[i+1],10):
        minor_ticks.append(j)


ax1.set_yticks(major_ticks)
ax1.set_yticks(minor_ticks, minor=True)
ax1.set_yticklabels([], minor=True)

ax1.grid(which="major",alpha=1)
ax1.grid(which="minor",alpha=0.3)
ax1.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))

ax2=ax1.twinx()
ax2.plot(space_volume, color="indigo", label="ordinary coordinate")
ax2.legend(loc='upper left', bbox_to_anchor=(0.1, 0.85))

plt.savefig('/results/space')
plt.show()