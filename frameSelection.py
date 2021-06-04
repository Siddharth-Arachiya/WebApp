from flask import Flask, render_template, Response, request, url_for, redirect, session
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import requests
import json
import re



from flask_socketio import SocketIO, emit
import io 
import base64
from PIL import Image
from io import StringIO
import numpy as np 
from engineio.payload import Payload
from DlibSocket import faceDlib

Payload.max_decode_packets = 500


app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*",ping_timeout=2, ping_interval=2)
 
#change
@app.route('/', methods=['POST', 'GET'])
def index():
    #url = "http://localhost:8080/video_feed_a?Glasses=None"  
    return render_template('start.html')


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
    

    #url = "http://20.193.229.188:8080/video_feed_a?Glasses=" + glass  
    return render_template('index1.html', title = title, brand = brand, desc = desc, price = price, cart = cart)


@socketio.on('image')
def image(arr):
    data_image = arr[0]
    #sbuf = StringIO()  #what are these lines for? are they necessary?
    #sbuf.write(data_image)

    # decode and convert into image
    #b = io.BytesIO(base64.b64decode(data_image)) #not used, replaced by next 2 lines
    #pimg = Image.open(b)
    im_bytes = base64.b64decode(data_image)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)

    ## converting RGB to BGR, as opencv standards
    #frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)


    # Process the image frame
    #frame = imutils.resize(frame, width=700)
    #frame = cv2.flip(frame, 1)
 

    imgencode=faceDlib(arr[1], frame)

    #imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
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