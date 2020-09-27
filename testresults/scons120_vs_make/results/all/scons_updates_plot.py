import matplotlib.pyplot as plt
files = [2500, 4500, 8500, 16500]
updatetime = [10.333, 18.711, 36.423, 1*60+18.569]
imptime = [6.958, 12.638, 25.455, 49.390]
#plt.plot(files, runtime, marker='o', linestyle='--', color='r', label='Square')
plt.plot(files, updatetime, marker='o', color='r', label='Update')
plt.plot(files, imptime, marker='o', color='g', label='ImplicitCached')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Updates')
plt.legend(loc='upper left')
plt.show()

