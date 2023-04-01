import serial
import time
import matplotlib.pyplot as plt
import itertools
import matplotlib.animation as animation
from typing import Dict, List
import pandas as pd
import datetime
import os

def get_data():
    def init():
        # set limits
        ax1.set_ylim(0, 100)
        ax1.set_xlim(0, 5)
        ax2.set_ylim(0, 2)
        ax2.set_xlim(0, 5)
        
        line1.set_data(xdata1, ydata1)
        line2.set_data(xdata2, ydata2)
        
        return line1,line2

    def data_gen():
        for cnt in itertools.count():
            t = cnt / 10

            while True:  
                d = ser.readline()
                if d:
                    string = d.decode()
                    if string != "": 
                        arr = string.split("\t")
                        k, f = float(arr[0]), float(arr[1])
                        break
                
            print(t, k, f)
            yield t, k, f

    def run(data):
        # update the data
        x, k, f = data

        # update knee angle data
        xdata1.append(x)
        ydata1.append(k)
        
        # update force data
        xdata2.append(x)
        ydata2.append(f)
        
        xmin1, xmax1 = ax1.get_xlim()
        xmin2, xmax2 = ax2.get_xlim()

        # checking if graph needs to shift
        if x >= xmax1:
            ax1.set_xlim(xmin1+5, xmax1+5)
            ax2.set_xlim(xmin2+5, xmax2+5)
            ax1.figure.canvas.draw()
            ax2.figure.canvas.draw()
        
        # set data
        line1.set_data(xdata1, ydata1)
        line2.set_data(xdata2, ydata2)

        return line1,line2

    
    # make sure the 'COM#' is set according the Windows Device Manager
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200, timeout=1)
    time.sleep(2)

    fig, (ax1, ax2) = plt.subplots(2)

    # initialize plots
    # fig, ax = plt.subplots()
    line1, = ax1.plot([], [], lw=2)
    line2, = ax2.plot([], [], lw=2)
    
    ax1.grid()
    ax2.grid()

    ax1.set_ylabel("Knee flexion angle")
    ax2.set_ylabel("Heel strike (0/1)")

    xdata1, ydata1 = [], []
    xdata2, ydata2 = [], []

    # Only save last 100 frames, but run forever
    ani = animation.FuncAnimation(fig, run, data_gen, init_func=init, interval=5)

    plt.show()

    # close port
    ser.close()

    return {
        "x": xdata1,
        "k": ydata1,
        "f": ydata2
    }

def save_data(data: Dict[str, List[float]]):
    """
    Save data to csv file. 

    Args:
        data (Dict[str, List[float]]): {x: [], k: [], f: []}
    """

    # convert to pandas df
    df = pd.DataFrame(data)
    
    # use current time for filename
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}.csv"
    
    # save to csv
    df.to_csv(path_or_buf=f"{os.getcwd()}/data/{filename}", index=False)

# if __name__ == "__main__":
    # get_data()

# things to do:
# -> connect with bluetooth
# -> look into cal sequence
# -> change axis values
