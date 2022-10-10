import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture("carPark.mp4") #Video_Feed

with open("CarParkPos", "rb") as f: #Opening the file we created for parking spaces
    posList = pickle.load(f)

width, height = 107, 48

# for cropping and checking of the parking space
def checkParkingSpace(imgPro):

    spaceCounter = 0

    for pos in posList: # For the pos of the parking spaces on the frames from the file we read above
        x,y = pos

        imgCrop = imgPro[y:y+height, x:x+width] #Getting the image of each seperate parking space

        count = cv2.countNonZero(imgCrop) #Countng the pixels in the image

        if count<900:
            color = (0,255,0) #Green
            thickness = 3
            spaceCounter+=1
        else:
            color = (0,0,255) #red
            thickness = 2

        cvzone.putTextRect(img,str(count), (x,y+height-3), scale = 1, thickness=2, offset=0, colorR = color) #Displaying pixels on the video

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) #Showing empty and filled parking spaces

    cvzone.putTextRect(img, f"Free Spaces: {spaceCounter}/{len(posList)}", (100,50), scale=2, thickness=4, offset=10,
                       colorR=(3, 252, 136))  # Displaying empty parking spaces on the video


s = True
while s:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): #For looping the video if it ends
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    #Processing the video for spaces detection
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3), 1)

    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16) #Converting an image to threshold binary image
    imgMedian = cv2.medianBlur(imgThreshold,5) # To remove the salt&pepper noise in the threshold image

    kernel = np.ones((3,3), np.uint8) #For generating kernel for dilating image
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1 ) #Dilating the image for better view of white parking space markings

    checkParkingSpace(imgDilate)



    cv2.imshow("Parking Lot", img)
    k = cv2.waitKey(10) & 0xFF  # Time/duration for which the image is to be opened

    if k == ord('q'):
        s = False
