import cv2
# opencv
import numpy as np
# numerical computations
import matplotlib.pyplot as plt
# plotting (at the end)

# importing libraries

backsub = cv2.BackgroundSubtractorMOG() 
#background subtraction to isolate moving cars


capture = cv2.VideoCapture("abbb.mp4") 
# reading video


i = 0
# car_count

minArea=1
# min area for removing unnecessary moments

kernel = np.ones((17,11),np.uint8)
# kernel for smoothening 


ff = 0
#current frame number

flag = False 


last_x = 0
last_y = 0

# setting threshold value
thx = 80
thy = 90 

all_pts  = []



# begining to read video.
try:
    while True:
        ret, frame = capture.read()
        orig = frame.copy()
        print frame.shape
        ff+=1 

        if ff > 600 :
            exit()

        

        pts = np.array([[0,0],[0,384],[200,0]], np.int32)
        cv2.fillPoly(frame, [pts], 2)
        # blacking out unnecessary video area.


        fgmask = backsub.apply(frame, None, 0.01)
        # applying background subtraction - creating mask


        # res = cv2.bitwise_and(frame,frame, mask= fgmask)
        # cv2.imshow('rr',res)


        erode=cv2.erode(fgmask,None,iterations=3) 
        # eroding noise.
        moments=cv2.moments(erode,True)   
        # finding moments

        area=moments['m00'] 
        # READ OPENCV DOCS - m00 gives area
        if moments['m00'] >=minArea:
            x=int(moments['m10']/moments['m00'])
            y=int (moments['m01']/moments['m00'])
            # above fomula gives centroid


            print 'X',x,'Y',y
            cv2.circle(frame,(x,y), 5, (0,0,255), -1)
            # centroid point by color RED
            cv2.rectangle(frame,(x-10,y-20),(x+10,y),(0,0,255),2)
            # creating square around point

        
            try :
                # incrementing car count only when there is an abrubt movement of the 
                # centroid point between consecutive frames along x,y

                # print 'X DIFF:',last_x - x,'Y DIFF:',last_y-y
                print abs(abs(last_x)+abs(last_y)-abs(x)-abs(y))

                all_pts.append([abs(abs(last_x)+abs(last_y)-abs(x)-abs(y)) , ff])

                if abs(abs(last_x)+abs(last_y)-abs(x)-abs(y)) > thx:
                    i = i+1 
                    print '*'*20,'PEAK!!!!','*'*20 , i
                else :
                    pass
            except :
                print 'ERROR'    
        
            last_x = x
            last_y = y

            # finding mean color in the rectangle drawn above. (can be done via numpy as well)
            for k in range(-10,10):
                for j in range(-20,0):
                    a ,aa , aaa= frame[k+x][j+y]
            a /= 400
            aa /= 400 
            aaa /= 400

            r,b,g = a , aa , aaa
            fflag = False
            b,g,r = frame[x,y-10]
            print (r,g,b)
            hsv = cv2.cvtColor(np.uint8([[[b,g,r]]]), cv2.COLOR_BGR2HSV)
            print hsv
            # hsv values are better for finding colorRanges. since "Value" is seperate 
            # from hue and saturation.


        cv2.putText(frame,'FRAME:'+ str(ff) + ' COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2)
        # showing Text onto frame.


        # cv2.line(frame,(650,0),(650,500),(255,0,0),1)


        # showing frame.
        cv2.imshow("Track", frame)  


        # out.write(frame)

        # cv2.circle(fgmask,(x,y), 5, (0,0,255), -1)
        # cv2.imshow("Background sub", fgmask)
        key = cv2.waitKey(100)
        if key == ord('q'):
                break

except:
    pass


cv2.destroyAllWindows()


# plotting the changes in the position of the centroid , since the count increases 
# when the changes are abrubt so , this can be verified by looking at the peaks 
# in the plot.

alpha = []
beta = []
for pt in all_pts:
    alpha.append(pt[0])
    beta.append(pt[1])
plt.plot(beta,alpha)
plt.show()