import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.pyplot import figure

# processes = [4, 8, 12, 16]
# runtime = [703.793, 529.981, 239.457, 226.168]

processes = [4, 8, 12, 16]
accuracy = [0.6735000014305115, 0.6603999733924866, 0.671500027179718, 0.6717000007629395]
accuracy2 = [0.6798999905586243, 0.6603999733924866, 0.7010999917984009, 0.7019000053405762]

figure(num=None, figsize=(6, 3),)
sns.set()
sns.set_context("paper")

plt.plot(np.array(processes), accuracy, 'violet', label="4 Nodes, 3 epochs")
plt.plot(np.array(processes), accuracy2, 'hotpink', label="2 Nodes, 6 epochs")
plt.fill_between(np.array(processes), accuracy, accuracy2, facecolor='pink', alpha=0.2)
plt.xlabel("Processors")
plt.ylim(0.64, np.max(accuracy2)*10.5/10)
plt.xlim(4, np.max(processes))
plt.ylabel("Accuracy")
plt.title("Accuracy Parallel CNN Cifar10")
plt.legend()
# plt.savefig("figs/4N-runtime.png", bbox_inches='tight')
plt.savefig("figs/2N-4N-accuracy.png", bbox_inches='tight')

plt.show()