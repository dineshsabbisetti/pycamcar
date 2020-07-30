code for image processing :

import cv2
import numpy as np
import requests
import urllib
# cap = cv2.VideoCapture(0)
url = "http://192.168.43.1:8080" # Your url might be different, check the app
cap = cv2.VideoCapture(url+"/video")
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
while True:
 _, frame = cap.read()
 hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 frame = cv2.line(frame,(200,0),(200,600),(255,0,0),2)
 frame = cv2.line(frame,(740,0),(740,600),(255,0,0),2)
 frame = cv2.line(frame,(200,250),(740,250),(255,0,0),2)
 # width = vs.get(3)
 # height = vs.get(4)
 # print("width",width)
 # print("hight=",height)
 
 lower_yellow = np.array([25,129,82])
 upper_yellow = np.array([150,255,255])

 yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

 (_,contours,_) = cv2.findContours(yellow_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

 for contour in contours:
  area = cv2.contourArea(contour)

  if(area > 800):
   x,y,w,h = cv2.boundingRect(contour)
   frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
   print("x=",(x + (x+w))/2)
   print("y=",(y + (y+h))/2)
   getx=(x + (x+w))/2
   gety=(y + (y+h))/2
   if(getx<200):
    print("left")
    r = requests.get('http://192.168.43.11/left')
    # print(r.content)
    break
   if(getx>740):
    print("right")
    r = requests.get('http://192.168.43.11/right')
    # print(r.content)
    break
   if((740>getx>200) and gety<250):
    print("forward") 
    r = requests.get('http://192.168.43.11/forward')
    # print(r.content) 
    break
   # if(gety>300 ):
   #  print("back") 
   #  r = requests.get('http://192.168.43.11/back')
   #  # print(r.content) 
   #  break
   if((740>getx>200) and gety>250):
    print("stop")
    r = requests.get('http://192.168.43.11/stop')
    # print(r.content) 
    break
 cv2.imshow("tracking", frame)
 cv2.imshow("color",yellow_mask )

 k = cv2.waitKey(5) & 0XFF
 if k == 27:
  break

cv2.destroyAllWindows()
cap.release()
