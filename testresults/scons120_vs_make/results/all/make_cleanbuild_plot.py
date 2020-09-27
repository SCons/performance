import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
buildtime = [57.79, 1*60+41.46, 3*60+11.77, 6*60+12.55]
plt.plot(files, buildtime, marker='o', color='b')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('make Build')
plt.legend(loc='upper left')
plt.show()

