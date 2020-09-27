import matplotlib.pyplot as plt
files = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
         10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
buildtime = [82.295, 124.347, 165.514, 207.538, 251.209, 296.519, 337.291, 381.367,
             427.404, 657.184, 900.210, 1161.363, 1423.762, 1690.425, 1961.193, 2247.942, 2535.374]
plt.plot(files, buildtime, marker='o', color='b')
plt.xlabel('C Files')
plt.ylabel('Time [s]')
plt.title('make Build')
plt.show()

