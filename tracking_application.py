import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd 
import os 

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        
        #Declare flags 
        self.flag_convert = 0
        self.flag_video = 0
        self.flag_color = False
        #Initialize buttons
        self.btn_video=tk.Button(self.window, text="Browse Videos", width=50, command=self.vid_name)
        self.btn_setPos=tk.Button(self.window, text="Set Reference Position", width=50, command=self.setPos)
        self.btn_display=tk.Button(self.window, text="Play Video", width=50, command=self.display_video)
        self.btn_track = tk.Button(self.window, text="Track Object", width=50, command=self.track_object)
        self.btn_color = tk.Button(self.window, text="Convert Color Space",width=50,command=self.color_space)
        self.btn_plot = tk.Button(self.window, text="Plot Position", width=50, command=self.plot_pos)
        self.btn_expPos = tk.Button(self.window, text="Export Position Data", width=50, command=self.exp_pos)
        self.btn_convert = tk.Button(self.window, text="Convert Position Data", width=50, command=self.convert)
        self.btn_expVid = tk.Button(self.window, text="Export Video", width=50, command=self.expVideo)
        self.btn_restart = tk.Button(self.window, text="Restart", width = 50, command=self.restart)
        self.btn_quit = tk.Button(self.window, text="Quit Program", width = 50, command=self.quit)

        #Pack Buttons
        self.btn_video.grid(row=0, column=0)
        self.btn_color.grid(row=4,column=0)
        self.pack_buttons()

        #Initiate loop
        self.window.mainloop()

    def pack_buttons(self):
        self.btn_display.grid(row=1, column = 0)
        self.btn_setPos.grid(row=2, column = 0)
        self.btn_track.grid(row=3, column = 0)
        
        self.btn_convert.grid(row=5, column = 0)
        self.btn_plot.grid(row=6, column = 0)
        self.btn_expPos.grid(row=7, column = 0)
        self.btn_expVid.grid(row=8, column = 0)
        self.btn_restart.grid(row=9, column=0)
        self.btn_quit.grid(row=10, column = 0)

    def unpack_buttons(self):
        self.btn_video.grid_remove()
        self.btn_display.grid_remove()
        self.btn_track.grid_remove()
        self.btn_color.grid_remove()
        self.btn_plot.grid_remove()
        self.btn_setPos.grid_remove()
        self.btn_expPos.grid_remove()
        self.btn_convert.grid_remove()
        self.btn_expVid.grid_remove()
        self.btn_restart.grid_remove()
        self.btn_quit.grid_remove()

    def color_space(self):
    	self.flag_color = True
    	self.unpack_buttons()
    	self.btn_color.grid_remove()
    	self.text = tk.Label(text="Converting Color Space")
    	self.text.grid()
    	self.vid.cnvtColorSpace()
    	self.text.grid_remove()
    	self.vid = Vid('color.mp4')
    	self.pack_buttons()

    def vid_name(self):
    	self.filepath = filedialog.askopenfilename(title = "Select A File", filetype =
        (("mp4 files","*.mp4"),("all files","*.*")) )
    	self.btn_video.grid_remove()
    	self.vid = Vid(self.filepath)	
    	self.filename = os.path.basename(self.filepath)
    	self.vid_title = self.filename[:-4]

    def expVideo(self):
        self.unpack_buttons()
        filename = self.vid_title+"track.mp4"
        saving = tk.Label(self.window, text="Saving as " + filename)
        saving.grid()
        self.vid.saveVideo(filename)
        saving.grid_remove()
        self.pack_buttons()

    def convert(self):
        self.flag_convert = 1
        self.set_data()
        ref = np.array(self.ref_point)
        rel = np.array(self.rel_point)
        self.rel_length = np.linalg.norm(ref - rel)
        self.unpack_buttons()
        
        def find_ratio():
            act_length = float(self.e2.get())
            self.ratio = act_length/self.rel_length
            print(self.ratio)
            for i in range(len(self.pos_x)):
                self.pos_x[i] = self.pos_x[i] * self.ratio
                self.pos_y[i] = self.pos_y[i] * self.ratio
            self.e2.grid_remove()
            self.btn_con.grid_remove()
            self.pack_buttons()

        self.e2 = tk.Entry(self.window)
        self.e2.insert(0, "Enter Actual Length")
        self.btn_con=tk.Button(self.window, text="Enter", width=25, command=find_ratio)

        self.e2.grid(row=0,column=0)
        self.btn_con.grid(row=0,column=1)

    def display_video(self):
        self.unpack_buttons()
        self.vid.play_video()
        self.pack_buttons()

    def set_data(self):
        x_list = np.array(self.vid.x_list)
        y_list = np.array(self.vid.y_list)
        w_list = np.array(self.vid.w_list)
        h_list = np.array(self.vid.h_list)
        self.pos_x = []
        self.pos_y = []
        self.frames = []
        for i in range(len(x_list)-1):
            self.frames.append(i+1)
            #self.pos_x.append((x_list[i] + w_list[i]/2) - self.ref_point(1))
            #self.pos_y.append(self.ref_point(2) - (y_list[i] + h_list[i]/2))
            self.pos_x.append((x_list[i] + w_list[i]/2))
            self.pos_y.append(self.vid.height - (y_list[i] + h_list[i]/2))
        self.pos_x = np.array(self.pos_x)
        self.pos_y = np.array(self.pos_y)

    def plot_pos(self):
        if self.flag_convert != 1:
            self.set_data()
        fig, ax = plt.subplots()
        for i in range(len(self.pos_x)):
            ax.scatter(self.pos_x[i], self.pos_y[i], c='black')
        ax.grid()
        ax.set(xlabel='X Position', ylabel ='Y Position', title='Position Plot')
        plt.show()

    def exp_pos(self):
        if self.flag_convert != 1:
            self.set_data()
        df = pd.DataFrame([self.frames, self.pos_x, self.pos_y], index=['Frames','X Position', 'Y Position']).T
        data = df.to_csv(self.vid_title+'tracking.csv', index = True)


    def setPos(self):
        (self.ref_point, self.rel_point) = self.vid.set_position()

    def restart(self):
    	if self.flag_color == True:
    		self.vid.__del__()
    		os.remove("color.mp4")
    	self.window.destroy()
    	App(tk.Tk(), "Tracking Application")

    def quit(self):
    	if self.flag_color == True:
    		self.vid.__del__()
    		os.remove("color.mp4")
    	self.window.destroy()

    def track_object(self):
        info = "Press F to play \n Press J to pause\n Left click for upper right crop \n Right click for lower right crop \n Press T to track \n Press J to stop track \n Press ENTER to exit"
        tk.messagebox.showinfo("Instructions", info)
        self.vid.track_object()

class Vid:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        #Values 
        self.total_frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.trim_start = 1
        self.trim_end = self.total_frames

        self.start = (0,0)
        self.end = (0,0)
        self.position = (0,0)
        self.rel_pos = (0,0)
        self.flag_rect = 0

        #track line initializatio
        self.x_list =[]
        self.y_list =[]
        self.w_list =[]
        self.h_list =[]
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            return (ret, frame)
        
    def play_video(self):
        cv2.namedWindow('Check App for Instructions',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Check App for Instructions', 1920,1080)
        self.set_framenumber(self.trim_start)
        draw = 1
        cnt = self.trim_start
        while True:
            key = cv2.waitKey(2)
            ret,frame = self.get_frame()
            if ret == True:
                frame = self.draw_circle_play(frame,draw)
                cv2.imshow('Check App for Instructions', frame)
                if cnt == self.trim_end:
                    break
                cnt = cnt + 1
                if draw < len(self.x_list):
                    draw = draw + 1
                if key == 13:
                    break
            else:
                break
        self.set_framenumber(self.trim_start)
        cv2.destroyAllWindows()

    def cnvtColorSpace(self):
    	out = cv2.VideoWriter('color.mp4',0x7634706d,self.fps,(self.width,self.height))
    	while True:
    		
    		ret, frame = self.get_frame()
    		if ret == True:
    			color = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    			y, cr, cb = cv2.split(color)
    			y_hist = cv2.equalizeHist(y)
    			cr_hist = cv2.equalizeHist(cr)
    			cb_hist = cv2.equalizeHist(cb)
    			color = cv2.merge((y_hist,cr_hist,cb_hist))
    			color = cv2.cvtColor(color,cv2.COLOR_YCrCb2BGR)
    			out.write(color)
    			if cv2.waitKey(25) & 0xFF == ord('q'): 
      				break
    		else:
    			break
    	out.release()


    def saveVideo(self, filename):
        out = cv2.VideoWriter(filename,0x7634706d,self.fps,(self.width,self.height))
        self.set_framenumber(self.trim_start)
        cnt = self.trim_start
        draw = 1
        while True:
            key = cv2.waitKey(2)
            ret, frame = self.get_frame()
            if ret == True:
                frame = self.draw_circle_play(frame,draw)
                out.write(frame)
                if cnt == self.trim_end:
                    break
                cnt = cnt + 1
                if draw < len(self.x_list):
                    draw = draw + 1
                if key == 13:
                    break
            else:
                break
        out.release()

    def set_framenumber(self, frame_number):
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start = (x,y)
        if event == cv2.EVENT_RBUTTONDOWN:
            self.end = (x,y)

    def click_event2(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.position = (x,y)
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rel_pos = (x,y)


    def play_loop(self):
        cnt = self.frame_num
        while True:
            key = cv2.waitKey(2)
            ret, frame = self.get_frame()
            if ret == True:
                cv2.imshow("Check App for Instructions", frame)
            if key == 106:
                self.frame_num = cnt
                break
            if key == 13:
                cv2.destroyAllWindows()
                break
            cnt = cnt + 1

    def draw_circle(self, frame):
        radius = 5
        color = (0,0,255)
        thickness = -1
        for i in range(len(self.x_list)):
            center_coordinates = (int(self.x_list[i] + self.w_list[i]/2), int(self.y_list[i] + self.h_list[i]/2))
            frame = cv2.circle(frame, center_coordinates, radius, color, thickness)
        return frame

    def draw_circle_play(self, frame, cnt):
        radius = 5
        color = (0,0,255)
        thickness = -1
        for i in range(cnt):
            center_coordinates = (int(self.x_list[i] + self.w_list[i]/2), int(self.y_list[i] + self.h_list[i]/2))
            frame = cv2.circle(frame, center_coordinates, radius, color, thickness)
        return frame


    def mean_shift_loop(self, frame):
        #Mean Shift Initialize 
        r,h,c,w = self.start[1],self.end[1]-self.start[1],self.start[0],self.end[0]-self.start[0]
        track_window = (c,r,w,h)
        roi = frame[r:r+h, c:c+w]
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        #Set frame count 
        cnt = self.frame_num
        while True:
            # Get Frame 
            ret, frame = self.get_frame()
            key = cv2.waitKey(2)
            # Mean Shift
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

            #Store ROI coordinates in lists
            x,y,w,h = track_window
            self.x_list.append(x)
            self.y_list.append(y)
            self.w_list.append(w)
            self.h_list.append(h)

            # Draw on image
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            frame = self.draw_circle(frame)

            cv2.imshow("Check App for Instructions",frame)
            cnt = cnt + 1
            #Press J to pause video 
            if key ==106: # J key to pause video
                self.frame_num = cnt
                #Store start and end values of ROI
                self.top = self.start 
                self.bottom = self.end
                #Reset flag values
                self.start = (0,0)
                self.end = (0,0)
                self.flag = 0
                #Set rectangle flag to one
                self.flag_rect = 1
                #Return the rectangle 
                return (x,y,w,h)
                break

    def track_object(self):
        cv2.namedWindow('Check App for Instructions',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Check App for Instructions', (self.width,self.height))
        cv2.setMouseCallback('Check App for Instructions', self.click_event)
        #Set variable to store frame number 
        self.frame_num = 1
        #Set Mean Shift Flag 
        self.flag = 0
        #Initialize loop 
        while True:
            #Set Key for button presses 
            key = cv2.waitKey(2)
            # Get Frame 
            ret, frame = self.get_frame();
            # Press F key to play 
            if key == 102:
                self.play_loop()
            #Select ROI 
            if self.start[0] > 0 and self.end[0] > 0:
                frame = cv2.rectangle(frame, self.start, self.end, (255, 0, 0), 2)
                if key == 116:
                    self.flag = 1
            #Start mean shift loop if T is pressed 
            if self.flag == 1:
                self.trim_start = self.frame_num
                (x,y,w,h) = self.mean_shift_loop(frame)
            if self.flag_rect == 1:
                frame = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
                frame = self.draw_circle(frame)
                if key == 13:
                    self.trim_end = self.frame_num
                    cv2.destroyAllWindows()
                    break
            #Frame number edge cases 
            if self.frame_num < 1:
                self.frame_num = 1
            if self.frame_num > self.total_frames:
                self.frame_num = 1
            #Display frame 
            if ret == True:
                cv2.imshow("Check App for Instructions", frame)
            #Set frame number
            self.set_framenumber(self.frame_num)
    
    def set_position(self):
        cv2.namedWindow('Check App for Instructions',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Check App for Instructions', (self.width,self.height))
        cv2.setMouseCallback('Check App for Instructions', self.click_event2)

        radius = 5
        color_red = (0,0,255)
        color_blue = (255,0,0)
        color_white = (255,255,255)
        thickness = -1

        clone = self.vid 
        ret, frame = clone.read()
        while True:
            key = cv2.waitKey(2)
            if ret == True:
                if self.position[0] != 0 and self.position[1] != 0:
                    frame = cv2.circle(frame, self.position, radius, color_red, thickness)
                if self.rel_pos[0] != 0:
                    frame = cv2.circle(frame, self.rel_pos, radius, color_blue, thickness)
                    frame = cv2.line(frame, self.rel_pos, self.position, color_white, 2)
                cv2.imshow('Check App for Instructions', frame)
            if key == 13:
                cv2.destroyAllWindows()
                return (self.position, self.rel_pos)
                break

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tk.Tk(), "Tracking Application")

