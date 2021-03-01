# BasketballTracking

Python program with goal of tracking a basketball and get position data for analysis purposes. 

Libararies used:
  Tkinter for GUI
  Opencv for computer vision tasks 
  Numpy for data operations
  Matplotlib for position plot 
  Pandas for .csv printing 

To run program:
From command line or IDE interface run 
  python tracking_application.py
  
Button explanation:
  Browse Videos: Opens dialog box to get video file 
  Play Video: Plays video from start of file if untracked or from start of track 
  Set Reference Position: Left click to set reference point and right click to get known distance
  Track Object: Opens warning with explanation of how to operate tracking and then opens video to track 
  Convert Color Space: If ball is hard to track, convert color space will use CMY conversion and histogram equalization to convert
    color space for tracking 
  Convert Position Data: If reference distance is known, input distance then data will be mapped from pixels to units inputted
  Plot Position: Plots position of tracked object
  Export Position Data: Exports position data to csv file with name of file + 'tracking.csv'
  Export Video: Exports Video of tracked object
  Restart: Restarts Application to perform another track 
  Quit Program: Quits Program 
  
Tracking Explanation: 
  Due to single plane of motion of basketball tracking, meanshift tracking algorithm was implemented using OpenCV's library   
  (https://docs.opencv.org/3.4/d7/d00/tutorial_meanshift.html). Since meanshift is sensitive to similar colors, the use of a convert
  color space can be used to convert to CMY color space, equalize histogram of certain channels, then use converted video to track
  object. 
  
Test Files Included:
  bball.mp4
  
NOTE: Some functions are hardcoded with certain parameters for the purpose of specific basketball trails such as set_data will change origin of pixel data from top left pixel to bottom left pixel as was needed for analysis. Also Color Space can be changed accordingly to get different results in tracking by changing which equalized histogram channels are merged into converted color video. 
