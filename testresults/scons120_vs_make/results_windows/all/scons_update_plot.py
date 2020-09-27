import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
buildtime = [24.917, 44.184, 84.059, 164.439]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Update')
plt.legend(loc='upper left')
plt.show()

