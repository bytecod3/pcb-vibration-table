from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import *
from data_types import NumericEntry
from hardware_bindings import HardwareBindings


class Application:
    def __init__(self, parent):
        # simulation parameters
        self.max_time = 0
        self.user_port = ""

        self.parent = parent

        # main window parameters
        self.parent.title("Vibration Table Client")

        # parent frame options
        self.parent_configs = {
            "bg": "#f0f0f0"
        }
        self.parent.config(self.parent_configs)

        # label config
        self.label_config = {

            "fg": "#434f62",
            "font": ("callibri", 10)
        }

        # input config
        self.input_config = {

            "font" : ("callibri", 10),
            "width" : 15,
            "relief" : RAISED
        }

        # button config
        self.button_config = {
            "fg": "#000005",
            "relief": RIDGE,
            "font": ("callibri", 10, "bold")
        }

        # frame configs
        self.frame_config = {
            "padx": "10",
            "pady": "10",
            "relief": RIDGE
        }

        self.create_widgets()

    def create_widgets(self):

        # get the serial port entered
        self.serial_port = StringVar()

        # get the simulation time in seconds
        self.sim_time = IntVar()

        # app frame
        self.main_frame = Frame(self.parent, padx=15, pady=15)
        self.main_frame.grid(column=0, row=0)

        # top app label
        self.app_label = Label(self.main_frame, text="Vibration Table Client", fg="#000000", padx=4, pady=10, font=("callibri", 15, "bold"))
        self.app_label.grid(column=0, row=0, columnspan=4)

        # create motor parameters label frame
        self.motor_parameters = LabelFrame(self.main_frame, self.frame_config, pady=15, text="Motor Specifications")
        self.motor_parameters.grid(column=0, row=1)

        # frequency
        self.frequency = Label(self.motor_parameters, self.label_config, text="Frequency: ")
        self.frequency.grid(column=0, row=0)
        self.frequency_lbl = Label(self.motor_parameters, self.label_config, text="60 Hz")
        self.frequency_lbl.grid(column=1, row=0)

        # RPM
        self.rpm = Label(self.motor_parameters, self.label_config, text="RPM: ")
        self.rpm.grid(column=0, row=1)
        self.rpm_lbl = Label(self.motor_parameters, self.label_config, text="20 000 /min")
        self.rpm_lbl.grid(column=1, row=1)

        self.rpm = Label(self.motor_parameters, self.label_config, text="Phase: ")
        self.rpm.grid(column=0, row=2)
        self.rpm_lbl = Label(self.motor_parameters, self.label_config, text="Single")
        self.rpm_lbl.grid(column=1, row=2)

        # serial connection parameters
        self.serial_port_frame = LabelFrame(self.main_frame, self.frame_config, text="Simulation Parameters")
        self.serial_port_frame.grid(column=0, row=2)

        self.serial_port_select_lbl = Label(self.serial_port_frame, self.label_config, text="Serial port:")
        self.serial_port_select_lbl.grid(column=0, row=0, pady=5, rowspan=1)

        self.serial_port_input = Entry(self.serial_port_frame, self.input_config, textvariable=self.serial_port)
        self.serial_port_input.grid(column=1, row=0, pady=5)

        self.simulation_time = Label(self.serial_port_frame, self.label_config, text="Simulation time (sec): ")
        self.simulation_time.grid(column=0, row=1)
        self.simulation_time_input = NumericEntry(self.serial_port_frame, textvariable=self.sim_time)
        self.simulation_time_input.config(self.input_config)
        self.simulation_time_input.grid(column=1, row=1)

        self.output_file_lbl = Label(self.serial_port_frame, self.label_config, text="Output folder: ")
        self.output_file_lbl.grid(column=0, row=2)

        # control buttons
        self.buttons_frame = Frame(self.main_frame, self.frame_config)
        self.buttons_frame.grid(column=0, row=3)

        self.run_btn = Button(self.buttons_frame, self.button_config, text="RUN", bg="green", font=("bold"), padx=25, command=self.start)
        self.run_btn.grid(column=0, row=0)

        self.stop_btn = Button(self.buttons_frame, self.button_config, text="STOP", bg="red", font=("bold"), padx=20)
        self.stop_btn.grid(column=0, row=1)

        # graphing canvas
        self.graphing_canvas_frame = Frame(self.main_frame, padx=15, pady=15)
        self.graphing_canvas_frame.grid(column=1, row=1)

    def start(self):
        """
        Check for valid simulation parameters
        Connect to arduino
        Open serial port
        Send command to start the motor
        Initialize graphing
        """

        # check for empty entries
        if not self.sim_time.get():
            # error message box
            flag = 1
            self.messenger(flag, "Empty simulation time", "Simulation time cannot be empty!")

        else:
            cap = 20  # maximum simulation time allowed 20 sec. todo: change cap
            if self.sim_time.get() > cap:
                self.max_time = cap
            else:
                self.max_time = self.sim_time.get()

        if not self.serial_port.get():
            flag = 1
            self.messenger(flag, "Empty serial port", "Serial port cannot be empty!")
        else:
            self.user_port = self.serial_port.get()

        # capitalize serial port
        print(self.user_port)
        print(self.max_time)

        vibrationObject = HardwareBindings(self.user_port, 9600, self.max_time)
        vibrationObject.update() # debug

    def messenger(self, flag,  title, message):
        if flag:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


def render_GUI():
    root = Tk()
    # root.geometry('600x200')
    # root.resizable(False, False)
    main = Application(root)

    # set icon here

    root.mainloop()

if __name__ == "__main__":
    render_GUI()
