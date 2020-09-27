import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
updatetime = [11.30, 20.32, 39.13, 1*60+20.38]
imptime = [8.26, 15.16, 29.12, 59.98]
plt.plot(files, updatetime, marker='o', color='r', label='Update')
plt.plot(files, imptime, marker='o', color='g', label='ImplicitCached')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Updates')
plt.legend(loc='upper left')
plt.show()

