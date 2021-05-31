from flask import Flask, render_template, Response, request, url_for, redirect, session
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import requests
import json
import re

app = Flask(__name__)
 
#change
@app.route('/')
def index():
    url = "http://20.204.16.86:8080/video_feed_a?Glasses=None"  
    return render_template('start.html', url = url)


@app.route('/start')
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
    

    url = "http://20.204.16.86:8080/video_feed_a?Glasses=" + glass  
    return render_template('index1.html', url = url, title = title, brand = brand, desc = desc, price = price, cart = cart)



"""@app.route('/video_feed_a')
def video_feed_a():
    glass = request.args.get("Glasses")
    return Response(faceDlib(glass), mimetype='multipart/x-mixed-replace; boundary=frame')"""

app.run(host='0.0.0.0',threaded=True)