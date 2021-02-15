import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure

# processes = [4, 8, 12, 16]
# runtime = [703.793, 529.981, 239.457, 226.168]

processes = [4, 8, 12, 16]
runtime = [703.793, 529.981, 239.457, 226.168]
runtime2 = [1019.281, 1056.461, 1041.992, 1071.729]

figure(num=None, figsize=(6, 3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(processes), runtime, 'violet', label="4 Nodes, 3 epochs")
plt.plot(np.array(processes), runtime2, 'hotpink', label="2 Nodes, 6 epochs")
plt.fill_between(np.array(processes), runtime, runtime2, facecolor='pink', alpha=0.2)
plt.xlabel("Processors")
plt.ylim(0, np.max(runtime2)*11/10)
plt.xlim(4, np.max(processes))
plt.ylabel("Total execution time (s)")
plt.title("Parallel CNN Cifar10")
plt.legend()
# plt.savefig("figs/4N-runtime.png", bbox_inches='tight')
plt.savefig("figs/2N-4N-runtime.png", bbox_inches='tight')

plt.show()
