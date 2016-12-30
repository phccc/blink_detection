import numpy as np
import matplotlib.pyplot as plt


def update_line(hl, axes, limit, x, y):
    if(x < limit):
        hl.set_xdata(np.append(hl.get_xdata(), x))
        hl.set_ydata(np.append(hl.get_ydata(), y))
        axes.set_ylim([0,np.max(hl.get_ydata())])
    else:
        y_temp = hl.get_ydata()
        y_temp = np.delete(y_temp, 0)
        y_temp = np.append(y_temp, y)
        hl.set_ydata(y_temp)
        axes.set_ylim([0,np.max(hl.get_ydata())])

"""
plt.axis([0, 10, 0, 1])
plt.ion()
hl, = plt.plot([],[])

for i in range(30):
    y = np.random.random()
    update_line(hl, 11, i, y)
    plt.draw()
    #plt.pause(0.05)
"""
