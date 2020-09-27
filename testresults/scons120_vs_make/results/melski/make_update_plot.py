import matplotlib.pyplot as plt
files = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
         10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
buildtime = [2.699, 4.611, 6.001, 7.980, 11.310, 16.226, 16.817, 20.424,
             25.023, 51.703, 90.747, 143.242, 194.337, 262.324, 340.391, 430.648, 530.847]
plt.plot(files, buildtime, marker='o', color='b')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('make Update')
plt.show()

