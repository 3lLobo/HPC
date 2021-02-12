import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


with open('results/q1.txt') as f:
    lines = f.readlines()[2:]

processes = [1, 2, 4, 8, 16]
runtime = [31.332232, 15.830318, 8.662756, 5.038685, 2.756245]


figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(processes), runtime, 'g', )
plt.fill_between(np.array(processes), runtime, facecolor='green', alpha=0.1)
plt.xlabel("Processors")
plt.ylim(0, np.max(runtime)*11/10)
plt.xlim(1, np.max(processes))
plt.ylabel("Total execution time (s)")
plt.title("MPI Vector-Matrix Multiplication (R=100, N=16000)")
plt.savefig("figs/runtime.png", bbox_inches='tight')

plt.show()