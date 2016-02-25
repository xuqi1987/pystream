# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
from flask import Flask
from flask import render_template
from flask import Response
from flask import url_for
from flask import flash
import datetime


app = Flask(__name__)
cap = cv2.VideoCapture(0)
app.secret_key = 'Test'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pic_now')
def current_picture():
    path = take_picture()
    return render_template('current_picture.html',path=path)


@app.route('/video_now')
def current_video():
    return render_template('video_push.html')

@app.route('/pic_list')
def pic_list():
    return render_template('pic_list.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():

    if cap.isOpened() == False:
        flash("摄像头没有打开")

    while True:
        ret, frame = cap.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),70]
        print len(cv2.imencode('.jpg', frame,encode_param))
        frame = cv2.imencode('.jpg', frame,encode_param)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def take_picture():
    ret, frame = cap.read()

    if cap.isOpened():
        frame = cv2.imencode('.jpg', frame)[1].tostring()
        #获得当前时间
        now = datetime.datetime.now()
        #转换为指定的格式:
        otherStyleTime = now.strftime("%Y%m%d_%H%M%S")
        pic_path = url_for('static',filename='pic/%s.jpg' % otherStyleTime)
        file_object = open(pic_path[1:], 'w')
        file_object.write(frame)
        file_object.close()
        return pic_path
    else:
        flash("摄像头没有打开",'error')

        return url_for('static',filename='pic/error.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)