import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
buildtime = [1*60+23.04, 2*60+48.19, 6*60+37.82, 16*60+59.24]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Build')
plt.legend(loc='upper left')
plt.show()

