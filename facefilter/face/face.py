#!/bin/python
import cv2, sys, os
from PIL import Image

dir = os.path.dirname(os.path.realpath(__file__))+"/"

def overlay(filename, file_overlay="happy.png"):
    print("Working on",filename)
    # read files
    cv_img = cv2.imread(filename)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    img  = Image.open(filename)
    overlay = Image.open(dir+file_overlay)

    # detect faces
    haar_face_cascade = cv2.CascadeClassifier(dir+'haarcascade_frontalface_alt.xml')
    faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.02);

    # overlay
    for (x, y, w, h) in faces:
        ol = overlay.resize((w*3//2,h*3//2), Image.ANTIALIAS)
        img.paste(ol, (x-w//4, y-h//4), ol)
    img.save("_"+filename)

if __name__ == "__main__":
    for a in sys.argv[1:]:
        overlay(a)