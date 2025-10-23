import cv2
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

imgBackground = cv2.imread('Resources/background.png')  

# Importing mode images into a list
folderModesPath = 'Resources/Modes/'
modePathList = os.listdir(folderModesPath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModesPath, path)))

# print(len(imgModeList))


while True:
    success, img = cap.read()

    # Image placement on background
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    # cv2.imshow("Webcam", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)
