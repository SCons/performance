import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
buildtime = [425.255, 730.854, 1151.060, 2161.544]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Build')
plt.legend(loc='upper left')
plt.show()

