import cv2
import pickle

width, height = 107, 48 #Dimensions of the rectangle required for creating parking space

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

# img = cv2.imread("carParkImg.png")

def mouseClick(events, x,y,flags,params):    #Mouse Events
    if events == cv2.EVENT_LBUTTONDOWN: #Click Left mouse button for creating and appending parking spaces
        posList.append((x,y))

    if events == cv2.EVENT_RBUTTONDOWN:  #Click Right Mouse button to delete space in case of a wrong parking spcae created
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                posList.pop(i)

    with open("CarParkPos", "wb") as f:    #Saving The parking spaces in a file
        pickle.dump(posList, f)

while True:

    # cv2.rectangle(img, (50,192), (157,240), (255,0,255),2)

    img = cv2.imread("carParkImg.png")

    for pos in posList:  #Creating and displaying a rectangle around the parking spaces we click on
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255,0,255),2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
