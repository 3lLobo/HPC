import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


with open('cluster-computing/results/q1.txt') as f:
    lines = f.readlines()[2:]

cpus = []
runtime = []

for line in lines:
    if len(line) == 6:
        continue
    if len(line) < 11:
        cpus.append(int(line[-3:]))
    else:
        runtime.append(float(line.split()[5]))

print(len(cpus))
print(np.max(cpus))
print(len(runtime))
print(np.max(runtime))

figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(cpus), runtime, 'g', )
plt.fill_between(np.array(cpus), runtime, facecolor='green', alpha=0.1)
plt.xlabel("Threads")
plt.ylim(0, np.max(runtime)*11/10)
plt.xlim(1, np.max(cpus))
plt.ylabel("Computing Time (s)")
plt.title(" Estimation of Pi")
plt.savefig("cluster-computing/lisa_threads1-24.png", bbox_inches='tight')

plt.show()