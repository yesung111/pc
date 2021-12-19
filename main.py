import cv2 as cv
import cvlib
import numpy as np
import serial
import time
from twilio.rest import Client
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import os

count = 0
unidentified = 0
unknown = 0

# twilio: sms 보내기
account_sid = 'AC665d172cc516181c7fe4004c6cd9377a'
auth_token = '2886fe7a4bb5d62c072cf9618a9223ac'
client = Client(account_sid, auth_token)

# Serial 통신
arduino = serial.Serial('COM4', 9600)
time.sleep(1)

# Open-CV 
cap = cv.VideoCapture(0, cv.CAP_DSHOW)

# OS
model = load_model('model.h5')
model.summary()

def save_img(img):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = timestr + '.png'
    cv.imwrite('result/' + timestr + '.png', img)

while True:
    if arduino.readable():
        val = arduino.readline()
        ppl = int(val.decode())

        if (int(ppl) == 1):
            print("Close")
            ret, frame = cap.read()
                      
            face, confidence = cvlib.detect_face(frame)
            if confidence:
                for idx, f in enumerate(face):
                    (startX, startY) = f[0], f[1]
                    (endX, endY) = f[2], f[3]
                    if 0 <= startX <= frame.shape[1] and 0 <= endX <= frame.shape[1] and 0 <= startY <= frame.shape[0] and 0 <= endY <= frame.shape[0]:
                        face_region = frame[startY:endY, startX:endX]
                    
                        face_region1 = cv.resize(face_region, (224, 224), interpolation = cv.INTER_AREA)
                        
                        x = img_to_array(face_region1)
                        x = np.expand_dims(x, axis=0)
                        x = preprocess_input(x)
                        
                        prediction = model.predict(x)

                        if prediction < 0.5:
                            print("Pass")
                            count += 1
                        else:
                            print("Unidentified")

                            cv.rectangle(frame, (startX,startY), (endX,endY), (0,0,255), 2)
                            Y = startY - 10 if startY - 10 > 10 else startY + 10
                            text = "Unidentified ({:.2f}%)".format((1 - prediction[0][0])*100)
                            cv.imwrite("result/%d.png"%count, frame)

                            message = client.messages.create(
                            to="+8201024078897", 
                            from_="+18722662398",
                            body="식별할 수 없는 사용자가 들어왔습니다!")
                            
            else:
                print("Unknown")
                cv.imwrite("result/%d.png"%count, frame)
                count += 1
                pmessage = client.messages.create(
                            to="+8201024078897", 
                            from_="+18722662398",
                            body="알 수 없는 움직임이 감지되었습니다!")