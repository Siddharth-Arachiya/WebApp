from flask import Flask, render_template, Response, request, url_for, redirect, session
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import requests
import json
import re
from flask_session import Session


from flask_socketio import SocketIO, emit
import io 
import base64
from PIL import Image
from io import StringIO
import numpy as np 
from engineio.payload import Payload
from DlibSocket import faceDlib

Payload.max_decode_packets = 500
#gimage = None
imdict = {}

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app,cors_allowed_origins="*",ping_timeout=20, ping_interval=2)
 
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("demoStart.html")

@app.route('/start', methods=['POST', 'GET'])
def start():

    glass=request.args.get("Glasses")

    try:
        req_str="https://aequm99.myshopify.com/admin/api/2021-04/products/" + glass + ".json?fields=title,body_html,variants"
        response1 = requests.get(req_str,auth=('5997eeb2ea13036b59f25dd280f73025', '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'))
        Pinfo=response1.json()

        try:
            title=Pinfo["product"]["title"].split("|")[0]
        except:
            title=Pinfo["product"]["title"]
        
        descr = Pinfo["product"]["body_html"]
        cleanr = re.compile('<.*?>')
        desc = re.sub(cleanr, '', descr)
        for m in re.finditer('\n\n\n', desc):
            if (m.start() > 20):
                desc = desc[:m.start()]
                break
        m2 = re.search('DESC', desc)
        if m2:
            desc = desc[:m2.start()]
        desc = desc.lstrip("\nDETAILS:\n")
        desc = desc.rstrip("\n")


        brand = "Brand: " + Pinfo["product"]["title"].split()[0]

        price = "\nPrice: Rs. " + Pinfo["product"]["variants"][0]["price"]

        vid = Pinfo["product"]["variants"][0]["id"]
        cart = "https://aequm99.myshopify.com/cart/" + str(vid) + ":1"
    except:
        title=''
        brand=''
        desc=''
        price =''
        cart =''
    

     
    return render_template('demoIndex1.html', title = title, brand = brand, desc = desc, price = price, cart = cart)


@socketio.on('image')
def image(arr):
    #global gimage
    data_image = arr[0]
    if data_image == "None":
        if data_image == "None":
        im_bytes = imdict[arr[2]]  #please add some check for if the image does not exist
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        #frame = gimage.copy()
    else:
        im_bytes = base64.b64decode(data_image)
        imdict[arr[2]]=im_bytes
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)

        frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        
        #gimage = frame.copy()
    
    imgencode=faceDlib(arr[1], frame)

    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)



"""@app.route('/video_feed_a')
def video_feed_a():
    glass = request.args.get("Glasses")
    return Response(faceDlib(glass), mimetype='multipart/x-mixed-replace; boundary=frame')"""

#app.run(host='0.0.0.0',threaded=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=80)