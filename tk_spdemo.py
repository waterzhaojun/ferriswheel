# This file works. let's move to v2 for further test.

import tkinter
import PIL.Image, PIL.ImageTk

import numpy as np

import serial
import time

# following add by Jun
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# , NavigationToolbar2TkAgg
matplotlib.use("TkAgg")
from matplotlib import style
style.use('ggplot')

f = plt.Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

class App(tkinter.Tk):
    def __init__(self, window_title, video_source=0):

        serial_speed = 115200
        self.serial_port = '/dev/cu.usbmodem1411' #'/dev/tty.usbmodem1411' #'/dev/cu.usbmodem1411' #
        self.buff = np.array([])
        self.memory_size = 1800
        self.savefolder = ''
        #self.ser = serial.Serial(serial_port, serial_speed, timeout = 1)

        tkinter.Tk.__init__(self)
        self.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        #self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self, width = 400, height = 300)
        self.canvas.grid(row=0, column=0)#.pack(side=tkinter.LEFT)

        # test plot canvus, by Jun
        
        runningcvs = FigureCanvasTkAgg(f, self)
        #runningcvs.show()
        runningcvs.get_tk_widget().grid(row=0, column=1)#.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand = True)

        # Button that lets the user take a snapshot
        self.btn_snapshot=ttk.Button(self, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=1)#pack(side=tkinter.TOP, expand=True)

        # Button to start plot
        self.startRec=ttk.Button(self, text="Start", width=50, command=self.record)
        self.startRec.grid(row=2)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()



    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            pass
            #cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def record(self):
        pass

    def update(self):
        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()

        #

        #if ret:
        #    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        #    self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.vid.set(3, 480)
        self.vid.set(4, 360)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
app = App("Tkinter and OpenCV")

ani = animation.FuncAnimation(f, animate, interval=100)
app.mainloop()