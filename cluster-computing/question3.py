import matplotlib.pyplot as plt

with open('results/q3.txt') as f:
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

plt.plot(cpus, speedup)
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.title(" Estimation of Pi LISA (1-24 threads)")
plt.savefig("2m_lisa_threads1-24.png")

plt.show()