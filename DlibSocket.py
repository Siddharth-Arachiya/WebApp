from flask import Flask, render_template, Response, request, url_for, redirect
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import dlib

detector=dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
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
        #yt=130;ht=300;xt=180;wt=300;
        #cropped_frame=frame[yt:yt+ht, xt:xt+wt]

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=detector(frame)
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            #cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),3)
            landmarks = predictor(frame,face)
            xl = landmarks.part(2).x
            yl = landmarks.part(2).y
            xr = landmarks.part(0).x
            yr = landmarks.part(0).y
            
            ratio=xr-xl
            
            xlf=int(xl-(0.4*ratio))
            xrf=int(xr+(0.4*ratio))
            ya=(yl+yr)/2
            yf1=int(ya-(0.35*ratio))
            yf2=int(ya+(0.35*ratio))
        
        

            face_glass_roi_color= frame[yf1:yf2, xlf:xrf]
            specs = cv2.resize(specs_ori, (xrf-xlf, yf2-yf1),interpolation=cv2.INTER_AREA)
            

            pos=(0, 0)
            scale=1
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
    
