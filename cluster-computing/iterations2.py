import matplotlib.pyplot as plt

with open('results/q2.txt') as f:
    lines = f.readlines()[3:-1]

result = [x.split(' ') for x in lines]
itera = []
runtime = []

for estimate in result:
    runtime.append(estimate[4])
    itera.append(estimate[6])


plt.plot(itera, runtime)
plt.xlabel("Leibniz Numbers")
plt.xticks(rotation=90)
plt.ylabel("Computing Time (s)")
plt.title("Estimation of Pi (24 threads)")
plt.tight_layout()
plt.savefig("Lisa_leibniz.png")

plt.show()