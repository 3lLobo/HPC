import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


processes = [1, 2, 4, 8, 16]
runtime = [31.332232, 15.830318, 8.662756, 5.038685, 2.756245] # R=100
runtime2 = [2.888114, 1.439575, 1.086268, 0.409414, 0.266661] # R=10
runtime3 = [382.938430, 164.401525, 89.849813, 51.758782, 29.860280] # R=1000
speedup = []
speedup2 = []
speedup3 = []

for r in range(len(runtime)):
    if r == 0:
        speedup.append(1)
        speedup2.append(1)
        speedup3.append(1)
        continue

    speedup.append(runtime[0]/runtime[r])
    speedup2.append(runtime2[0]/runtime2[r])
    speedup3.append(runtime3[0]/runtime3[r])

rel_speedup = []
rel_speedup2 = []

for s in range(len(speedup)):
    if s == 0:
        rel_speedup.append(0)
        rel_speedup2.append(0)
        continue

    rel_speedup.append(speedup[s]-speedup[s-1])



# print(cpus)
# print(runtime)

figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(processes), speedup, 'g', label="R=100")
plt.plot(np.array(processes), speedup2, 'r', label="R=10")
plt.plot(np.array(processes), speedup3, 'deeppink', label="R=1000" )
# plt.fill_between(np.array(speedup2), speedup, facecolor='green', alpha=0.1)
plt.xlabel("Processors")
plt.ylabel("Speedup")
plt.ylim(0, np.max(speedup)*11/10)
plt.xlim(1, np.max(processes))
plt.title("Speedup of MPI Vector-Matrix multiplication (N=16000)")
plt.legend()
plt.savefig("figs/speedup-multiple.png", bbox_inches='tight')

plt.show()