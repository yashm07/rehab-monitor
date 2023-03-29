import serial
import time
import matplotlib.pyplot as plt
import itertools
import matplotlib.animation as animation

def init():
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 5)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

def data_gen():
    for cnt in itertools.count():
        t = cnt / 10

        while True:  
            d = ser.readline()
            if d:
                string = d.decode()
                if string != "": 
                    y = float(string)
                    break
            
        print(t, y)
        yield t, y

def run(data):
    # update the data
    x, y = data

    xdata.append(x)
    ydata.append(y)
    
    xmin, xmax = ax.get_xlim()

    # checking if graph needs to zoom out
    if x >= xmax:
        ax.set_xlim(xmin+5, xmax+5)
        ax.figure.canvas.draw()
    
    # set data
    line.set_data(xdata, ydata)

    return line,

if __name__ == "__main__":
    # make sure the 'COM#' is set according the Windows Device Manager
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200, timeout=1)
    time.sleep(2)

    # initialize plots
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []

    # Only save last 100 frames, but run forever
    ani = animation.FuncAnimation(fig, run, data_gen, init_func=init, interval=5)

    plt.show()

    # close port
    ser.close()