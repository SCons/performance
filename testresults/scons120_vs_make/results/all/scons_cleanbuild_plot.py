import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
buildtime = [1*60+23.74, 2*60+50.04, 6*60+37.86, 17*60+4.72]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Build')
plt.legend(loc='upper left')
plt.show()

