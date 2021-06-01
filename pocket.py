from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io 
import base64
from PIL import Image
from io import StringIO
import cv2
import numpy as np 
import imutils
from engineio.payload import Payload
from DlibSocket import faceDlib

Payload.max_decode_packets = 500


app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*",ping_timeout=20, ping_interval=2)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('socketIndex.html')

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    #frame = imutils.resize(frame, width=700)
    #frame = cv2.flip(frame, 1)
 

    imgencode=faceDlib("6687620038844", frame)

    #imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')