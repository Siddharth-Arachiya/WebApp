from flask import Flask, render_template, Response, request, url_for, redirect 
from DlibModel import faceDlib




app=Flask(__name__)

@app.route('/video_feed_a')

def video_feed_a():
    #th.start()
    glass = request.args.get("Glasses")
    return Response(faceDlib(glass), mimetype='multipart/x-mixed-replace; boundary=frame')




app.run(host='0.0.0.0',port=8080, debug=True)