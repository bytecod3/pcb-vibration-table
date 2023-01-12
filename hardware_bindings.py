"""
This class contains all hardware functions to control the vibration table
"""
import serial
from collections import deque


class HardwareBindings:
    def __init__(self, serial_port, baud, max_length):
        self.ser = serial.Serial(serial_port, baud)
        self.max_length = max_length

        # init deque to buffer most recent values
        self.x_values = deque([0.0]*self.max_length)
        self.y_values = deque([0.0]*self.max_length)
        self.z_values = deque([0.0]*self.max_length)

    def buffer(self, data):
        """
        Get 3 values from serial port (x, y, z)
        Add this values to respective buffers
        """
        assert(len(data) == 3)
        self.add_to_deque(self.x_values, data[0])
        self.add_to_deque(self.y_values, data[1])
        self.add_to_deque(self.z_values, data[2])

    def add_to_deque(self, buf, val):
        """
        Remove the oldest value from the tail of the buffer deque
        Insert newest value at the head of the buffer deque
        """
        buf.pop()
        buf.appendleft()

    def stop(self):
        pass

    def serial_init(self):
        pass

    def save_to_file(self):
        pass

    def close(self):
        """
        Clean up the serial port
        """
        self.ser.flush()
        self.ser.close()

