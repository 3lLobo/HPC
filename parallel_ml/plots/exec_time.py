import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


processes = [4, 8, 12, 16]
runtime = [703.793, 529.981, 239.457, 226.168]
runtime2 = [1019.281, 1056.461, 1041.992, 1071.729]
speedup = []
speedup2 = []

for r in range(len(runtime)):
    if r == 0:
        speedup.append(1)
        speedup2.append(1)
        continue

    speedup.append(runtime[0]/runtime[r])
    speedup2.append(runtime2[0]/runtime2[r])

# print(cpus)
# print(runtime)

figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(processes), speedup, 'violet', label="N=4, epochs=3")
plt.plot(np.array(processes), speedup2, 'hotpink', label="N=2, epochs=6")
plt.fill_between(np.array(processes), speedup, speedup2, facecolor='pink', alpha=0.2)
plt.xlabel("Processors")
plt.ylabel("Speedup")
plt.ylim(0.8, np.max(speedup)*11/10)
plt.xlim(4, np.max(processes))
plt.title("Speedup of CNN classifying CIFAR10")
plt.legend()
plt.savefig("figs/speedup-multiple-CNN.png", bbox_inches='tight')

plt.show()