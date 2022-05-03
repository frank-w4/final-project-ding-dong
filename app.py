#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import datetime
from email_img import email_pic
from email_911 import email_emergency
global img_count
global img_arr
img_count = 0
img_cap = 9999
# import camera driver
"""
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera
"""

from camera_opencv import Camera

app = Flask(__name__)

os.system("rm ./cap_pics/*")


@app.route('/', methods=["GET", "POST"])
def index():
    global img_count
    global img_cap
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # Let's grab the current time and date
        current_time = datetime.datetime.now()
        time=current_time.strftime("%H:%M:%S")
        day=current_time.strftime("%m.%d.%Y")
        tot_day=day+time
    
    if request.form['action'] == "Take Picture":
        print("Take Picture")       
        os.system("cp ./tmp/" + str(img_count-3) + ".jpg ./cap_pics")
        email_pic(str(img_count-3))
    elif request.form['action'] == "Unlock Door":
        print("Unlock Door")
    elif request.form['action'] == "Call 911":
        print("Call 911")
        os.system("cp ./tmp/" + str(img_count-3) + ".jpg ./cap_pics")
        email_emergency(str(img_count-3))
    else:
        print("Bad Parameter")
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        global img_count
        print("Image (from app.py) Count " + str(img_count))
        print("..........."+str(img_cap) + "//" + str(img_count) + "...........")
        frame = camera.get_frame()
        img_count = img_count + 1
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
