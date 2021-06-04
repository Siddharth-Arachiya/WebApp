from flask import Flask, render_template, Response, request, url_for, redirect
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2



face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def faceDlib(glass,frame1):
    #detector=dlib.get_frontal_face_detector()
    #predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    

    try:
        frame = frame1
    #frame = imutils.resize(frame, width=500)
    except Exception as e:
        print(e)

    try:
        specs_ori = cv2.imread("static/resources/" + glass + ".png", -1)
    except:
        (flag, encodedImage)=cv2.imencode(".jpg",frame)
        return(encodedImage)


    if (glass == "None") or (specs_ori is None):
        pass
    else:        
        yt=130;ht=300;xt=180;wt=300
        cropped_frame=frame[yt:yt+ht, xt:xt+wt]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(cropped_frame, 1.2, 5, 0, (120, 120), (350, 350))
        for (x, y, w, h) in faces:
            if h > 0 and w > 0:
                y=y+yt;  x=x+xt; 
                glass_symin = int(y + 1.2 * h / 5)
                glass_symax = int(y + 2.6 * h / 5)
                sh_glass = glass_symax - glass_symin
                face_glass_roi_color = frame[glass_symin:glass_symax, x+10:x+w-10]
                specs = cv2.resize(specs_ori, (w-20, sh_glass),interpolation=cv2.INTER_CUBIC)
                pos=(0, 0)
                scale=1

                specs = cv2.resize(specs, (0, 0), fx=scale, fy=scale)
                h, w, _ = specs.shape  # Size of foreground
                rows, cols, _ = face_glass_roi_color.shape  # Size of background Image
                y, x = pos[0], pos[1]  # Position of foreground/overlay image


            # loop over all pixels and apply the blending equation
                for i in range(h):
                    for j in range(w):
                        if x + i >= rows or y + j >= cols:
                            continue
                        alpha = float(specs[i][j][3] / 255.0)  # read the alpha channel
                        face_glass_roi_color[x + i][y + j] = alpha * specs[i][j][:3] + (1 - alpha) * face_glass_roi_color[x + i][y + j]
            


                       
    (flag, encodedImage)=cv2.imencode(".jpg",frame)
    return(encodedImage)
    
