# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
from flask import Flask,render_template,Response,url_for,flash,request,redirect

import datetime
from camera import Camera


app = Flask(__name__)
app.secret_key = 'Test'
cam = Camera(0)

@app.route('/')
def index():
    return render_template('index.html')

# 拍照取的图片
@app.route('/pic_now')
def current_picture():
    path = cam.take_picture(url_for('static',filename='pic'))
    return render_template('current_picture.html',path=path)

@app.route('/video_now')
def current_video():
    return render_template('video_push.html')

@app.route('/pic_list/')
def pic_list():
    piclist = cam.get_all_picture()
    return render_template('pic_list.html',piclist=piclist)

@app.route('/del_pic/<name>')
def del_pic(name):
    cam.del_pic(name)
    return redirect(url_for('pic_list'))

@app.route('/video_feed')
def video_feed():
    return Response(cam.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)