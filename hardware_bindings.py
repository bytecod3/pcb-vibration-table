"""
This class contains all hardware functions to control the vibration table
"""
import serial
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import csv
from time import sleep


class HardwareBindings:
    def __init__(self, serial_port, baud, max_time, max_length=100):
        self.ser = serial.Serial(serial_port, baud)
        self.max_length = max_length
        self.max_time = max_time

        # init deque to buffer most recent values
        self.x_values = deque([0.0]*self.max_length)
        # self.y_values = deque([0.0]*self.max_length)
        # self.z_values = deque([0.0]*self.max_length)

    def buffer(self, data):
        """
        Get 3 values from serial port (x, y, z)
        Add this values to respective buffers
        """
        # assert(len(data) == 3)
        self.add_to_deque(self.x_values, data[0])
        # self.add_to_deque(self.y_values, data[1])
        # self.add_to_deque(self.z_values, data[2])

    def add_to_deque(self, buf, val):
        """
        Remove the oldest value from the tail of the buffer deque
        Insert newest value at the head of the buffer deque
        """
        buf.pop()
        buf.appendleft()

    def close(self):
        """
        Clean up the serial port
        """
        self.ser.flush()
        self.ser.close()

    def process_data(self):

        i = 0
        while i < 5:

            input_data = self.ser.read()
            print(float(input_data))

            # add data to deque
            # # todo: assert for length = 3
            # self.buffer(data)

            i += 1
            sleep(1)

        time = [0, 1, 2]
        x_vals = [23, 55, 34]

        zipped_data = zip(time, x_vals)
        # write to file
        with open('simulation_data.csv', 'w') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(zipped_data)

    #
    # def animate(self):
    #     # set up animation
    #     fig = plt.figure()
    #     ax = plt.axes(xlim=(0, self.max_time), ylim=(0, 1023)) # todo: change 1023
    #     x, = ax.plot([], [])
    #
    #     anim = animation.FuncAnimation(fig, self.update, fargs=(x,), interval=10)
    #
    #     plt.show()
    #
    #     self.close()


    def stop(self):
            pass
