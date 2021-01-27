import matplotlib.pyplot as plt

with open('results/q1.txt') as f:
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

print(cpus)
print(runtime)

plt.plot(cpus, runtime)
plt.xlabel("Threads")
plt.ylabel("Computing Time (s)")
plt.title(" Estimation of Pi")
# plt.savefig("lisa_threads1-24.png")

plt.show()