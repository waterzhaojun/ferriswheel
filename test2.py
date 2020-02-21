import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

# following add by Jun
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# , NavigationToolbar2TkAgg
matplotlib.use("TkAgg")
from matplotlib import style
style.use('ggplot')

class App(tkinter.Tk):
    def __init__(self, window_title, video_source=0):
        tkinter.Tk.__init__(self)
        self.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0)#.pack(side=tkinter.LEFT)

        # test plot canvus, by Jun
        f = plt.Figure(figsize=(self.vid.width/100,self.vid.height/100), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,65,6,4,6])
        runningcvs = FigureCanvasTkAgg(f, self)
        #runningcvs.show()
        runningcvs.get_tk_widget().grid(row=0, column=1)#.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand = True)

        # Button that lets the user take a snapshot
        self.btn_snapshot=ttk.Button(self, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=1)#pack(side=tkinter.TOP, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()



    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

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
app.mainloop()