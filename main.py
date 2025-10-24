import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

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

# Load the encoding file 
print("Loading Encoding File...")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encoding Loaded Successfully")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) 
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Image placement on background
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("Face Distance: ", faceDis)
        # print("Face Matches: ", matches)

        # matchIndex = faceDis.argmin()

        # if matches[matchIndex]:
        #     # print("Known Face Detected")
        #     studentId = studentIds[matchIndex].upper()
        #     # print(studentId)

        #     y1, x2, y2, x1 = faceLoc
        #     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #     cv2.rectangle(imgBackground, (55 + x1, 162 + y1), (55 + x2, 162 + y2), (0, 255, 0), 2)
        #     cv2.rectangle(imgBackground, (55 + x1, 162 + y2 - 35), (55 + x2, 162 + y2), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(imgBackground, studentId, (55 + x1 + 6, 162 + y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
        #                 (255, 255, 255), 2)
    
        matchIndex = np.argmin(faceDis)
        # print("Match Index:", matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected")
            # print(studentIds[matchIndex])

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            imgBackground = cvzone.cornerRect(imgBackground, (55 + x1, 162 + y1, x2 - x1, y2 - y1), rt=0)

    # cv2.imshow("Webcam", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)
