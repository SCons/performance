import matplotlib.pyplot as plt
files = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
         10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
buildtime = [172.762, 273.197, 381.336, 499.577, 625.730, 757.848, 903.929, 1054.580,
             1215.052, 2113.091, 3231.252, 4622.466, 6222.696, 8179.577, 10309.083, 12602.104, 17789.959]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Build')
plt.show()

