import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math
pullups = 0
cap = cv2.VideoCapture('pullups.mov')
pd = PoseDetector(trackCon= 0.70, detectionCon= 0.70)
def angles(lmlist,p1,p2,p3,p4,p5,p6,drawpoints , ):
    global a , b, c , angle, pullups
    if len(lmlist) != 0:
        point1 = lmlist[p1]
        point2 = lmlist[p2]
        point3 = lmlist[p3]
        point4 = lmlist[p4]
        point5 = lmlist[p5]
        point6 = lmlist[p6]

        x1,y1 = point1[0:2]
        x2,y2 = point2[0:2]
        x3,y3 = point3[0:2]
        x4,y4 = point4[0:2]
        x5,y5 = point5[0:2]
        x6,y6 = point6[0:2]
       
        a = np.sqrt((x1 - x3)**2+(y1 - y3)**2)
        b = np.sqrt((x3 - x5)**2+(y3 - y5)**2)
        c = np.sqrt((x1 - x5)**2+(y1 - y5)**2)
        angle = (c**2 - b**2 - a**2)/(2*b*a*-1)
        
        
        
   

        if drawpoints == True:
            cv2.circle(frame,(x1,y1),10,(0,0,255),5)
            cv2.circle(frame,(x2,y2),10,(0,0,255),5)
            cv2.circle(frame,(x3,y3),10,(0,0,255),5)
            cv2.circle(frame,(x4,y4),10,(0,0,255),5)
            cv2.circle(frame,(x5,y5),10,(0,0,255),5)
            cv2.circle(frame,(x6,y6),10,(0,0,255),5)
 ## if angle from wrist elbow and shoulder is less than 20*, count a pull up.
        if abs(angle - 0.945) < 1e-3:
            pullups+=1
                 
           
    


while True:
    ret, frame = cap.read()
    if not ret:
        # cap = cv2.VideoCapture('pullups.mov')
        continue
    frame = cv2.resize(frame, (800,1000))
    pd.findPose(frame, draw = 1)
    lmlist , bbox = pd.findPosition(frame, draw = 1, bboxWithHands= 0)
    angles(lmlist,11,12,13,14,15,16,True,)

   
    cv2.putText(frame , "pullups done:" + str(pullups) ,(10 , 800) ,cv2.FONT_HERSHEY_COMPLEX  , 2 , (0,150,255) , 2)
    cv2.imshow('frame', frame)    
  

    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()