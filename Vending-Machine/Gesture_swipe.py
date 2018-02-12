
# coding: utf-8

# In[ ]:
import time
import os
import sys
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

def nothing(x):
    pass

def fetch_content(a):
    return a

p=sys.stdin.readline()


HSV_TrackBar = np.zeros([100,700], np.uint8)


#### STEP 1: SET HSV VALUES ACC TO VENUE

cv2.namedWindow("HSV_TrackBar")
cv2.createTrackbar('L_h', 'HSV_TrackBar',0,179,nothing)
cv2.createTrackbar('L_s', 'HSV_TrackBar',0,255,nothing)
cv2.createTrackbar('L_v', 'HSV_TrackBar',0,255,nothing)

cv2.createTrackbar('H_h', 'HSV_TrackBar',179,179,nothing)
cv2.createTrackbar('H_s', 'HSV_TrackBar',255,255,nothing)
cv2.createTrackbar('H_v', 'HSV_TrackBar',255,255,nothing)

start = time.time()

time_P = 5


while True:
    ret, frame = cam.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    
    L_h = cv2.getTrackbarPos('L_h', 'HSV_TrackBar')
    L_s = cv2.getTrackbarPos('L_s', 'HSV_TrackBar')
    L_v = cv2.getTrackbarPos('L_v', 'HSV_TrackBar')
    
    H_h = cv2.getTrackbarPos('H_h', 'HSV_TrackBar')
    H_s = cv2.getTrackbarPos('H_s', 'HSV_TrackBar')
    H_v = cv2.getTrackbarPos('H_v', 'HSV_TrackBar')
    
    
    L_h = 45
    L_s = 39
    L_v = 51
    
    lower_color = np.array([L_h, L_s, L_v])
#     lower_color = np.array([108, 23, 82])


    upper_color = np.array([H_h, H_s, H_v])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    blur = cv2.medianBlur(mask, 5)
    
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    hsv_d = cv2.dilate(blur, kernel)
    
    
    _,contours,_ = cv2.findContours(hsv_d, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE,)   
    
    max_area = -10000
    c_index = 0
    
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if(area > max_area):
            max_area = area
            c_index = i
    
    largest_contour = contours[c_index]
    hull = cv2.convexHull(largest_contour)
    
    cv2.drawContours(frame,contours,c_index, (0,0,255),2)
    cv2.drawContours(frame,[hull],-1,(0,255,255),2)
  

    hullIndices = cv2.convexHull(largest_contour, returnPoints = False)
    
    defects = cv2.convexityDefects(largest_contour, hullIndices)
    

    if(L_h > 10 and L_s >10 and L_v >0):

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(largest_contour[s][0])
            end = tuple(largest_contour[e][0])
            far = tuple(largest_contour[f][0])
    #         cv2.line(frame,start,end,[255,0,0],2)
            cv2.line(frame,start,far,[255,0,0],2)
            cv2.line(frame,far,end,[255,0,0],2)
            cv2.circle(frame,far,5,[0,255,0],-1)


        max_d = -9999
        poi = (0, 0)
        x, y, w, h = cv2.boundingRect(largest_contour)
        for tracing_height in range(int(y+0.3*h), y+h):
            for tracing_width in range(int(x+0.3*w), x+w):
                distance = cv2.pointPolygonTest(largest_contour, (tracing_width, tracing_height), True)

                if(max_d<distance):
                    max_d = distance
                    poi = (tracing_width, tracing_height)


        finger_tips = []

        for i in range(len(hull)):            
                x = hull[i][0][0]
                y = hull[i][0][1]

                x_prev = hull[i-1][0][0]
                y_prev = hull[i-1][0][1]

                dist1 = np.sqrt((x - x_prev)**2 + (y - y_prev)**2)

                if(dist1 > 20):
                    finger_tips.append((x_prev,y_prev))

    #     print(finger_tips[0][0])
        cx = poi[0]
        cy = poi[1]

        i =0 
        while(i < len(finger_tips)):            
            dist2 = np.sqrt((finger_tips[i][0]- cx)**2 + (finger_tips[i][1] - cy)**2)
            if(dist2 < 2*max_d or dist2 > 3.8*max_d or finger_tips[i][1] > cy+max_d):
                finger_tips.remove((finger_tips[i][0],finger_tips[i][1]))
            else:
                i = i+1


   
        for k in range(len(finger_tips)):
            cv2.circle(frame,finger_tips[k],10,[0,0,0],2)
            cv2.line(frame,poi,finger_tips[k],[255,255,0],2)
            
#         value_recieved = False
        
#         if(str(len(finger_tips)) == '5'):
#             value_recieved = True
#             break   
            
#         else:
#             continue
                     
    
        cv2.putText(frame, str(len(finger_tips)),(6,100), cv2.FONT_HERSHEY_DUPLEX,4,(0,0,0),2,cv2.LINE_AA)
        
        # ans = fetch_content(len(finger_tips))
        print(len(finger_tips))
        


#     cv2.imshow('p', hsv_d)


    # cv2.imshow('o', frame)
    # if p == 'q':
    #     break
  #  if time.time() > start + time_P :
  #      break





    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows() 


# In[ ]:



