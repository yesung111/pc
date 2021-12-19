import cv2 as cv
import cvlib
import argparse

parser = argparse.ArgumentParser(description= "등록 프로그램입니다.")

parser.add_argument('--dir', required = True, help = "영상 경로를 입력하세요")
parser.add_argument('--name', required = True, help = "영상 이름을 입력하세요")
parser.add_argument('--save', required = True, help = "저장 경로를 입력하세요")

args = vars(parser.parse_args())

dir = args["dir"] + '/'
value = dir + args["name"]
save = args["save"]

vid = cv.VideoCapture(value)

count = 0
while True:
  ret, frame = vid.read()

  faces, confidence = cvlib.detect_face(frame)

  for idx, face in enumerate(faces):

    (startX, startY) = face[0], face[1]
    (endX, endY) = face[2], face[3]
    img = frame[startY:endY:, startX:endX, :]


    cv.imwrite(save + '%d.png' % count, img)
    print('%d saved'% count)
    if cv.waitKey(0) ==27:
      break
    count +=1
  if not ret:
    print("stopped")
    break

vid.release()

