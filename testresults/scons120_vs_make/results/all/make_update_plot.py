import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
updatetime = [1.01, 2.00, 4.28, 10.10]
plt.plot(files, updatetime, marker='o', color='b')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('make Update')
plt.show()

