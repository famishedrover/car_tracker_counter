import cv2
import numpy as np
import matplotlib.pyplot as plt
backsub = cv2.BackgroundSubtractorMOG() #background subtraction to isolate moving cars
capture = cv2.VideoCapture("abbb.mp4") #change to destination on your pc 
i = 0
minArea=1
kernel = np.ones((17,11),np.uint8)
ff = 0 
flag = False 
last_x = 0
last_y = 0
thx = 80
thy = 90 

all_pts  = []

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.cv.CV_FOURCC(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (288,384))


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



        fgmask = backsub.apply(frame, None, 0.01)

        # res = cv2.bitwise_and(frame,frame, mask= fgmask)
        # cv2.imshow('rr',res)


        erode=cv2.erode(fgmask,None,iterations=3) 
        moments=cv2.moments(erode,True)   

        area=moments['m00'] 
        if moments['m00'] >=minArea:
            x=int(moments['m10']/moments['m00'])
            y=int (moments['m01']/moments['m00'])
            print 'X',x,'Y',y
            cv2.circle(frame,(x,y), 5, (0,0,255), -1)
            cv2.rectangle(frame,(x-10,y-20),(x+10,y),(0,0,255),2)

        
            try :
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



        cv2.putText(frame,'FRAME:'+ str(ff) + ' COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2)

        # cv2.line(frame,(650,0),(650,500),(255,0,0),1)

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

alpha = []
beta = []
for pt in all_pts:
    alpha.append(pt[0])
    beta.append(pt[1])
plt.plot(beta,alpha)
plt.show()