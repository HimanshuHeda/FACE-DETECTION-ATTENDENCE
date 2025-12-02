import pandas as pd
import os
import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import numpy as np
from supabase import create_client, Client
from datetime import datetime

# Replace with your Supabase project URL and API key
SUPABASE_URL = "URL"
SUPABASE_KEY = "Key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    print("Camera read success:", success)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the Data from Supabase
                response = supabase.table("students").select("*").eq("id", id).execute()
                studentInfo = response.data[0] if response.data else None
                print(studentInfo)
                # Download image only if new student detected
                imgStudent = None
                if studentInfo is not None:
                    for ext in [".png", ".jpg", ".JPG"]:
                        try:
                            img_response = supabase.storage.from_("images").download(f"Images/{id}{ext}")
                            array = np.frombuffer(img_response, np.uint8)
                            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                            if imgStudent is not None:
                                imgStudent = cv2.resize(imgStudent, (216, 216))
                                break
                        except Exception:
                            continue
                    if imgStudent is None:
                        print(f"Image for student {id} not found in Supabase Storage.")
                # Update data of attendance
                if studentInfo is not None:
                    last_attendance_time = studentInfo['last_attendance_time']
                    try:
                        datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%dT%H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        studentInfo['total_attendance'] += 1
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        supabase.table("students").update({"total_attendance": studentInfo['total_attendance'], "last_attendance_time": now_str}).eq("id", id).execute()

                        # Log attendance to Excel sheet
                        excel_path = "attendance_records.xlsx"
                        record = {
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Time": datetime.now().strftime("%H:%M:%S"),
                            "ID": id,
                            "Name": studentInfo['name'],
                            "Major": studentInfo['major'],
                            "Year": studentInfo['year'],
                            "Standing": studentInfo['standing'],
                            "Attendance": studentInfo['total_attendance']
                        }
                        if os.path.exists(excel_path):
                            df = pd.read_excel(excel_path)
                            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
                        else:
                            df = pd.DataFrame([record])
                        df.to_excel(excel_path, index=False)
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                else:
                    print(f"No student info found for id {id} in Supabase database.")

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10 and studentInfo is not None:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    if imgStudent is not None:
                        imgStudentResized = cv2.resize(imgStudent, (216, 216))
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudentResized

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break   