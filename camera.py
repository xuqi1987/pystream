# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
import datetime
import os
from flask import flash

class Camera():

    def __init__(self,num):
        self.cap = cv2.VideoCapture(num)
        self.pic_list = None
        pass

    def take_picture(self,path):
        ret, frame = self.cap.read()

        if self.cap.isOpened():
            frame = cv2.imencode('.jpg', frame)[1].tostring()
            #获得当前时间
            now = datetime.datetime.now()
            #转换为指定的格式:
            otherStyleTime = now.strftime("%Y%m%d_%H%M%S")
            path = path +'/'+otherStyleTime +'.jpg'
            print path
            file_object = open(path[1:], 'w')
            file_object.write(frame)
            file_object.close()
            return path
        else:
            return ('static/img/error.png')

    def gen(self):

        while True:
            ret, frame = self.cap.read()
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),70]
            print len(cv2.imencode('.jpg', frame,encode_param))
            frame = cv2.imencode('.jpg', frame,encode_param)[1].tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def  get_all_picture(self):
            root = os.getcwd() + '/static/pic/'
            self.pic_list = []
            pic_path_ab = []

            for x in os.listdir(root):
                self.pic_list.append(root + x)
                pic_path_ab.append(x)

            return pic_path_ab

    def del_pic(self,name):
        for item in self.pic_list:
            # 查找还有name的路径
            if item.count(name):
                os.remove(item)
                self.pic_list.remove(item)
