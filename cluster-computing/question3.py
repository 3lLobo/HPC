import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


with open('cluster-computing/results/q3.txt') as f:
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

speedup = []

for r in range(len(runtime)):
    if r == 0:
        speedup.append(1)
        continue

    speedup.append(runtime[0]/runtime[r])

rel_speedup = []

for s in range(len(speedup)):
    if s == 0:
        rel_speedup.append(0)
        continue

    rel_speedup.append(speedup[s]-speedup[s-1])


print(cpus)
print(runtime)

figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(cpus), speedup, 'g', )
plt.fill_between(np.array(cpus), speedup, facecolor='green', alpha=0.1)
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.ylim(0, np.max(speedup)*11/10)
plt.xlim(1, np.max(cpus))
plt.title(" Estimation of Pi LISA (1-24 threads)")
plt.savefig("cluster-computing/2m_lisa_threads1-24.png", bbox_inches='tight')

plt.show()