# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
from flask import Flask
from flask import render_template
from flask import Response
from flask import url_for
import datetime

app = Flask(__name__)
cap = cv2.VideoCapture(1)

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

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.imencode('.jpg', frame)[1].tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            frame = cv2.imread(url_for('static',filename='pic/error.png'),0)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def take_picture():
    ret, frame = cap.read()

    if ret:
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
        return url_for('static',filename='pic/error.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0',processes=1)