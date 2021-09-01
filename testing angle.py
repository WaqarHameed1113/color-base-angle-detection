import cv2
import math

path='img_1.png'
img=cv2.imread(path)

pointList=[]
cv2.imshow('Image',img)
def mousepoints(event,x,y,flags,params):
    if event==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)
        pointList.append([x,y])
        #cv2.imshow('Image',img)
        print(x,y)

def gradient(pt1,pt2):
    return ((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))

def getAngle(pointlist):
    pt1,pt2,pt3=pointlist[-3:]
    m1=gradient(pt1,pt2)
    m2=gradient(pt1,pt3)
    angR=math.atan((m2-m1)/(1+(m1*m2)))
    angD=round(math.degrees(angR))
    print(math.fabs(angD))
cv2.setMouseCallback('Image',mousepoints)
while True:

    if len(pointList)==3:
        getAngle(pointList)
        pointLis=[]

    cv2.imshow('Image',img)

    if  cv2.waitKey(1) & 0xFF == ord('q'):
        pointList=[]
        img = cv2.imread(path)

