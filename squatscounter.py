
import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math
import time

squats = 0
limit = 1
in_range = False
def count(lmlist , p1, p2 ,p3,p4, drawpoint):
    global squats, limit , in_range
    if len(lmlist) != 0:
        point1 = lmlist[p1]
        point2 = lmlist[p2]
        point3 = lmlist[p3]
        point4 = lmlist[p4]

        x1,y1 = point1[0:2]
        x2,y2 = point2[0:2]
        x3,y3 = point3[0:2]
        x4,y4 = point4[0:2]
        line = (int)((y1+y2)/2)
        if(y3 <= line):
            in_range = True
        else:
            in_range = False
            if limit == squats:
                 limit = limit + 1
        
        if (squats < limit) and (in_range):
             squats = squats + 1

            

        if drawpoint == True:
                cv2.circle(frame,(x1,y1),10,(0,0,255),3)
                cv2.circle(frame,(x2,y2),10,(0,0,255),3)



cap = cv2.VideoCapture("sqats.mov")
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (800,1000))
    pd.findPose(frame,draw = 1)
    lmlist , bbox = pd.findPosition(frame, draw = 1, bboxWithHands= 0)  
    count(lmlist,23,24,25,26,True)
    cv2.putText(frame ,"squats done = " + str(squats), (10,800), cv2.FONT_HERSHEY_COMPLEX  , 2 , (120,150,255) , 2 )
    cv2.imshow('frame', frame) 
    
    
    if(cv2.waitKey(1) == 'q'):
        
        break



cv2.destroyAllWindows()