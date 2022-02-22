import matplotlib.pyplot as plt

class Graph_IV():

    def __init__(self, x = [], y = [], y2 = []):
        self.x = x
        self.y = y
        self.y2 = y2
        self.xlim = [0, 0]
        self.ylim = [0, 0]
        self.ylim2 = [0, 0]
        self.xlabel = "Time(s)"
        self.ylabel = "Current(A)"
        self.ylabel2 = "Voltage(V)"


    def export(self, filename):
        plt.savefig(filename)
        return

    def print(self):
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax2 = self.ax.twinx()
        try:
            self.ax.set_xlim([min(min(self.x), self.xlim[0]), max(max(self.x), self.xlim[1])])
            self.ax.set_ylim([min(min(self.y), self.ylim[0]), max(max(self.y), self.ylim[1])])
            self.ax2.set_xlim([min(min(self.x), self.xlim[0]), max(max(self.x), self.xlim[1])])
            self.ax2.set_ylim([min(min(self.y2), self.ylim2[0]), max(max(self.y2), self.ylim2[1])])
        except ValueError:
            pass
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.line1, = self.ax.plot(self.x, self.y, color = "C0")
        self.line2, = self.ax2.plot(self.x, self.y2, color = "C1")
        self.ax2.set_ylabel(self.ylabel2)
        return

    def update(self, newx, newy, newy2):
        self.x.append(newx)
        self.y.append(newy)
        self.y2.append(newy2)
        self.ax.set_xlim([min(min(self.x), self.xlim[0]), max(max(self.x), self.xlim[1])])
        self.ax.set_ylim([min(min(self.y), self.ylim[0]), max(max(self.y), self.ylim[1])])
        self.ax2.set_xlim([min(min(self.x), self.xlim[0]), max(max(self.x), self.xlim[1])])
        self.ax2.set_ylim([min(min(self.y2), self.ylim2[0]), max(max(self.y2), self.ylim2[1])])
        self.line1.set_xdata(self.x)
        self.line1.set_ydata(self.y)
        self.line2.set_xdata(self.x)
        self.line2.set_ydata(self.y2)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        return
