import matplotlib.pyplot as plt
files = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
         10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
buildtime = [34.612, 52.530, 71.134, 90.092, 109.432, 128.069, 148.940, 169.922,
             190.099, 297.412, 413.601, 546.191, 693.908, 879.492, 1074.860, 1264.096, 1448.356]
plt.plot(files, buildtime, marker='o', color='g')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('SCons Update')
plt.show()

