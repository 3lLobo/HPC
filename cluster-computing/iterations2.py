import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure


with open('cluster-computing/results/q2.txt') as f:
    lines = f.readlines()[3:-1]

result = [x.split(' ') for x in lines]
itera = []
runtime = []

itera.append(0.)
runtime.append(0.)
for estimate in result:
    runtime.append(float(estimate[4]))
    itera.append(float(estimate[6])/1000000.)


figure(num=None, figsize=(6,3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(itera), runtime, 'g', )
plt.fill_between(np.array(itera), runtime, facecolor='green', alpha=0.1)
plt.xlabel("Leibniz Numbers $10^6$")
plt.ylabel("Computing Time (s)")
plt.ylim(0, np.max(runtime)*11/10)
plt.xlim(0, np.max(itera))
plt.title("Estimation of $\pi$ (24 threads)")

plt.savefig("cluster-computing/Lisa_leibniz.png", bbox_inches='tight')

plt.show()
