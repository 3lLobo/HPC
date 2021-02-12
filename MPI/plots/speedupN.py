import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


processes = [1, 2, 4, 8, 16]
runtime = [0.000021, 0.000138, 0.000348, 0.000696, 0.001255] # N=16
runtime2 = [0.003407, 0.002649, 0.001895,  0.061205, 0.090883] # N=160
runtime3 = [0.271762, 0.144929, 0.075682, 0.101519, 0.482740] # N=1600
runtime4 = [31.332232, 15.830318, 8.662756, 5.038685, 2.756245] # N=16000

speedup = []
speedup2 = []
speedup3 = []
speedup4 = []

for r in range(len(runtime)):
    if r == 0:
        speedup.append(1)
        speedup2.append(1)
        speedup3.append(1)
        speedup4.append(1)
        continue

    speedup.append(runtime[0]/runtime[r])
    speedup2.append(runtime2[0]/runtime2[r])
    speedup3.append(runtime3[0]/runtime3[r])
    speedup4.append(runtime4[0]/runtime4[r])

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

plt.plot(np.array(processes), speedup, 'g', label="N=16")
plt.plot(np.array(processes), speedup2, 'r', label="N=160")
plt.plot(np.array(processes), speedup3, 'deeppink', label="N=1600" )
plt.plot(np.array(processes), speedup4, 'palegreen', label="N=16000" )
# plt.fill_between(np.array(speedup2), speedup, facecolor='green', alpha=0.1)
plt.xlabel("Processors")
plt.ylabel("Speedup")
plt.ylim(0, 12)
plt.xlim(1, np.max(processes))
plt.title("Speedup of MPI Vector-Matrix multiplication (R=100)")
plt.legend()
plt.savefig("figs/speedup-N.png", bbox_inches='tight')

plt.show()